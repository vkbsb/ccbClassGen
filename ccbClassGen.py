import plistlib
import sys
import os

"""
memberVarAssignmentName # this will give the name of the variable.
memberVarAssignmentType # 1 we need, 0 we dont' need
if we encounter a controlbutton or a menuitem we need to pick the 
function name from properties.
"""
def getVariables(node):
    members = []
    methods = []
    ctrlmethods = []
    children = node["children"]
    for child in children:
        if child["memberVarAssignmentType"] == 1:
            member = {}
            member['name'] = child["memberVarAssignmentName"]
            member['class'] = child['baseClass'].replace("CC", "", 1)           
            members.append(member)
        #iterate over the children of child.
        cchildren = child["children"]
        if len(cchildren) > 0:
            (cmembers, cmethods, cctrlmethods) = getVariables(child)
            members += cmembers
            methods += cmethods
            ctrlmethods += cctrlmethods

        props = child["properties"]
        for prop in props:
            if prop["name"] == "ccControl" and prop["type"] == "BlockCCControl":
                val = prop["value"]
                ctrlmethods.append(val[0])
            if prop["name"] == "block" and prop["type"] == "Block":
                val = prop["value"]
                methods.append(val[0])
    return (members, methods, ctrlmethods)

def getCPP(cname, bcname, members, methods, ctrlmethods):
    cppcontents = """
#include "{ClassName}.h"
{ClassName}* {ClassName}::getNewInstance() {{
    /* Create an autorelease NodeLoaderLibrary. */
    NodeLoaderLibrary * ccNodeLoaderLibrary = NodeLoaderLibrary::newDefaultNodeLoaderLibrary();

    ccNodeLoaderLibrary->registerNodeLoader("{ClassName}", %sLoader::loader());

    /* Create an autorelease CCBReader. */
    cocosbuilder::CCBReader * ccbReader = new cocosbuilder::CCBReader(ccNodeLoaderLibrary);
    ccbReader->setCCBRootPath("res/");
    auto node = ccbReader->readNodeGraphFromFile("res/{ccbiFile}");
    node->setPosition(Director::getInstance()->getWinSize()/2);

    node->setUserObject(NULL);
    ccbReader->autorelease();

    return dynamic_cast<{ClassName}*>(node);
}}

cocos2d::SEL_MenuHandler {ClassName}::onResolveCCBCCMenuItemSelector(cocos2d::Ref * pTarget, const char* pSelectorName)
{{
""".format(ClassName=cname, ccbiFile=os.path.basename(fpath).replace("ccb", "ccbi")) 

    #CCB_SELECTORRESOLVER_CCMENUITEM_GLUE(this, "buttonClicked", SmileKpi::buttonClicked);
    for method in set(methods):
        cppcontents += "    CCB_SELECTORRESOLVER_CCMENUITEM_GLUE(this, {Function}, {ClassName}::{Function});".format(Function=method, ClassName=cname)

    cppcontents += """
    return nullptr;
}}

Control::Handler {ClassName}::onResolveCCBCCControlSelector(cocos2d::Ref * pTarget, const char* pSelectorName)
{{
""".format(ClassName=cname, ccbiFile=os.path.basename(fpath).replace("ccb", "ccbi")) 

    for method in set(ctrlmethods):
        cppcontents += "    CCB_SELECTORRESOLVER_CCCONTROL_GLUE(this, \"%s\", %s::%s);\n" % (method, cname, method)

    cppcontents += """
    return nullptr;
}}

bool {ClassName}::init()
{{
    if(!{BaseClass}::init()){{
        return false;
    }}

    return true;
}}

void {ClassName}::onEnter()
{{
    {BaseClass}::onEnter();
}}

void {ClassName}::onExit()
{{
    {BaseClass}::onExit();
}}

bool {ClassName}::onAssignCCBMemberVariable(cocos2d::Ref* pTarget, const char* pMemberVariableName, cocos2d::Node* pNode)
{{
""".format(ClassName=cname, BaseClass=bcname)

    for member in members:
        cppcontents += "    CCB_MEMBERVARIABLEASSIGNER_GLUE(this, \"{name}\", {class} *, {name});\n".format(**member)
    
    cppcontents += """
    return false;
}

"""
    #add the member functions to the class
    for method in set(methods):
        cppcontents +="void {ClassName}::{Method}(Ref* pSender){{\n\tlog(\"{ClassName}::{Methdo}\");\n}}".format(ClassName=cname, Method=method)

    for method in set(ctrlmethods):
        cppcontents += "void {ClassName}::{Method}(cocos2d::Ref *pSender, Control::EventType pControlEvent){{\n\tlog(\"{ClassName}::{Method}\");\n}}".format(ClassName=cname, Method=method)

    return cppcontents

def getHPP(cname, bcname, members, methods, ctrlmethods):
    hcontents = """
#ifndef __{ClassName}__
#define __{ClassName}__

#include <iostream>
#include "cocos2d.h"
#include "cocos-ext.h"
#include "cocosbuilder/CocosBuilder.h"
USING_NS_CC;
USING_NS_CC_EXT;
using namespace cocosbuilder;

class {ClassName} : public {BaseClass},  public CCBSelectorResolver, public CCBMemberVariableAssigner
{{
    //variables come here.
""".format(ClassName=cname, BaseClass=bcname) 

    #add the member variables to the class
    for member in members:
        hcontents += "    {class} * {name}\n".format(**member)

    hcontents += """
    public:
    bool init();
    virtual void onEnter();
    virtual void onExit();

    virtual cocos2d::SEL_MenuHandler onResolveCCBCCMenuItemSelector(cocos2d::Ref * pTarget, const char* pSelectorName);
    virtual Control::Handler onResolveCCBCCControlSelector(cocos2d::Ref * pTarget, const char* pSelectorName);
    virtual bool onAssignCCBMemberVariable(cocos2d::Ref* target, const char* memberVariableName, cocos2d::Node* node);

    //member functions for callbacks.
"""
    #add the member functions to the class
    for method in set(methods):
        hcontents +="   void {}(Ref* pSender);\n".format(method)

    for method in set(ctrlmethods):
        hcontents += "    void {0}(cocos2d::Ref *pSender, Control::EventType pControlEvent);\n".format(method)

    #tailend of the header file.
    hcontents += """
    ~{ClassName}();
    CREATE_FUNC({ClassName});

    static {ClassName}* getNewInstance();
}};

class {ClassName}Loader : public {BaseClass}Loader {{
    public:
        CCB_STATIC_NEW_AUTORELEASE_OBJECT_METHOD({ClassName}Loader, loader);

        CCB_VIRTUAL_NEW_AUTORELEASE_CREATECCNODE_METHOD({ClassName});
}};

#endif /* defined(__{ClassName}__) */ 
""".format(ClassName=cname, BaseClass=baseClass) 
    return hcontents

if __name__ == '__main__': 
    if len(sys.argv) < 2:
        print ("Please provide the ccb file")
        sys.exit(1)

    fpath = sys.argv[1]

    ccb = plistlib.readPlist(fpath)


    nodeGraph = ccb["nodeGraph"]
    ccbClass = nodeGraph["customClass"]

    (members, methods, ctrlmethods) = getVariables(nodeGraph)
    baseClass = nodeGraph["baseClass"].replace("CC", "", 1)
    hpp = getHPP(ccbClass, baseClass, members, methods, ctrlmethods)
    cpp = getCPP(ccbClass, baseClass, members, methods, ctrlmethods)

    cppfname = ccbClass + ".cpp"
    hppfname = ccbClass + ".h"
    try: 
        fp = open(cppfname, "r")
        print "file {0} exists please delete it or move it.".format(cppfname)
        fp.close()
    except:
        fp = open(cppfname, "w")
        fp.write(cpp)
        fp.close()

        fp = open(hppfname, "w")
        fp.write(hpp)
        fp.close()
        
