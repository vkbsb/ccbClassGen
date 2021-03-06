#!/usr/bin/python

import plistlib
import sys
import os

SCRIPT_HOME = "CLASSGEN_HOME"

def getNodeProp(node, propName):
    props = node["properties"]
    for prop in props:
        if prop["name"] == propName:
            return prop
    return None


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

            #LabelTTF,BMP will all be just Label.
            if member['class'].startswith('Label'):
                member['class'] = 'Label';

            #ensure that we do not add members that do not have names set.
            if member['name']:
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

def getCPP(cname, bcname, members, methods, ctrlmethods, sequences):
    ccbfile = os.path.basename(fpath).replace("ccb", "ccbi");

    cpp_template_file = open(os.path.join(os.environ[SCRIPT_HOME], 'template.cpp'))
    cpp_template = cpp_template_file.read()
    cpp_template_file.close()
    
    mig = "CCB_SELECTORRESOLVER_CCMENUITEM_GLUE"
    cig = "CCB_SELECTORRESOLVER_CCCONTROL_GLUE"

    menuitem_glue = "\n"
    for method in set(methods):
        menuitem_glue += "    {Mig}(this, \"{Function}\", {ClassName}::{Function});\n".format(Mig=mig, Function=method, ClassName=cname)

    control_glue = "\n"
    for method in set(ctrlmethods):
        control_glue += "    %s(this, \"%s\", %s::%s);\n" % (cig, method, cname, method)
    
    default_anim = -1;
    for seq in sequences:
        if seq['autoPlay']:
            default_anim = seq['sequenceId']

    member_init = "\n"
    for member in members:
        member_init += "    {name} = NULL;\n".format(**member)

    member_glue = "\n"
    for member in members:
        member_glue += "    CCB_MEMBERVARIABLEASSIGNER_GLUE(this, \"{name}\", {class} *, {name});\n".format(**member)
    
    #animation check for user input functions disable inputs when CCB is animating.
    anim_check = """
    //remove this check if you want button to work when animation is playing.
    if( _isAnimating ){
        return;
    }
    """
    member_functions = ""
    #add the member functions to the class
    for method in set(methods):
        member_functions +="""
void {ClassName}::{Method}(Ref* pSender){{
    {AnimCheck}
    log(\"{ClassName}::{Method}\");
}}
""".format(AnimCheck=anim_check, ClassName=cname, Method=method)

    for method in set(ctrlmethods):
        member_functions += """
void {ClassName}::{Method}(cocos2d::Ref *pSender, Control::EventType pControlEvent)
{{
    {AnimCheck}
    log(\"{ClassName}::{Method}\");
}}
""".format(AnimCheck=anim_check, ClassName=cname, Method=method)

    member_destroy = "\n"
    for member in members:
        member_destroy += "    CC_SAFE_RELEASE({name});\n".format(**member)
    
    obj = {}
    obj["ClassName"] = cname
    obj["BaseClass"] = bcname
    obj["ccbiFile"] = ccbfile
    obj["MenuItemGlue"] = menuitem_glue
    obj["ControlItemGlue"] = control_glue
    obj["MemberVariablesInit"] = member_init
    obj["MemberVariableGlue"] = member_glue
    obj["MemberFunctions"] = member_functions
    obj["MemberVariablesDestroy"] = member_destroy
    obj["DefaultAnimSequence"] = default_anim

    cppcontents = cpp_template.format(**obj)

    return cppcontents

def getHPP(cname, bcname, members, methods, ctrlmethods, sequences):
    hpp_template_file = open(os.path.join(os.environ[SCRIPT_HOME], 'template.h'))
    hpp_template = hpp_template_file.read()
    hpp_template_file.close()
 
    anim_enum = ""
    for seq in sequences:
        seq["name"] = seq["name"].upper().replace(" ", "_")
        anim_enum += "{name} = {sequenceId}, ".format(**seq)
    anim_enum = anim_enum[:-2];
    
    #add the member variables to the class
    member_vars = ""
    for member in members:
        member_vars += "    {class} * {name};\n".format(**member)

    class_methods = ""
    #add the member functions to the class
    for method in set(methods):
        class_methods +="   void {}(Ref* pSender);\n".format(method)

    for method in set(ctrlmethods):
        class_methods += "  void {0}(cocos2d::Ref *pSender, Control::EventType pControlEvent);\n".format(method)

    obj = {}
    obj["ClassName"] = cname
    obj["BaseClass"] = bcname
    obj["MemberVariables"] = member_vars
    obj["ClassMethods"] = class_methods
    obj["AnimsEnum"] = anim_enum
    hcontents = hpp_template.format(**obj)

    return hcontents 

if __name__ == '__main__': 
    if len(sys.argv) < 2:
        print ("Please provide the ccb file")
        sys.exit(1)

    fpath = sys.argv[1]

    if not (SCRIPT_HOME in os.environ):
        import inspect, os
        print inspect.getfile(inspect.currentframe()) # script filename (usually with path)
        path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) # script director
        os.environ[SCRIPT_HOME] = path

    ccb = plistlib.readPlist(fpath)

    nodeGraph = ccb["nodeGraph"]
    ccbClass = nodeGraph["customClass"]
    baseClass = nodeGraph["baseClass"].replace("CC", "", 1)
    sequences = ccb["sequences"]

    (members, methods, ctrlmethods) = getVariables(nodeGraph)

    #remove the duplicates in methods / ctrlmethods and members
    members = {v['name']:v for v in members}.values()
    methods = set(methods)
    ctrlmethods = set(ctrlmethods)

    #generate the header / cpp files
    hpp = getHPP(ccbClass, baseClass, members, methods, ctrlmethods, sequences)
    cpp = getCPP(ccbClass, baseClass, members, methods, ctrlmethods, sequences)

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
        
