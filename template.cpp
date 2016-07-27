#include "{ClassName}.h"

{ClassName}* {ClassName}::getNewInstance() {{
    /* Create an autorelease NodeLoaderLibrary. */
    NodeLoaderLibrary * ccNodeLoaderLibrary = NodeLoaderLibrary::newDefaultNodeLoaderLibrary();

    ccNodeLoaderLibrary->registerNodeLoader("{ClassName}", {ClassName}Loader::loader());

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
    {MenuItemGlue}

    return nullptr;
}}

Control::Handler {ClassName}::onResolveCCBCCControlSelector(cocos2d::Ref * pTarget, const char* pSelectorName)
{{
    {ControlItemGlue}
    return nullptr;
}}

bool {ClassName}::init()
{{
    if(!{BaseClass}::init()){{
        return false;
    }}
    
    {MemberVariablesInit}

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
    {MemberVariableGlue}

    return false;
}}

{MemberFunctions}

{ClassName}::~{ClassName}()
{{
    {MemberVariablesDestroy}
}}

