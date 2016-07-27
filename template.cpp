#include "{ClassName}.h"

Scene * {ClassName}::createScene()
{{
    Scene *pscene = Scene::create();
    pscene->addChild({ClassName}::getNewInstance());
    return pscene;
}}

{ClassName}* {ClassName}::getNewInstance() {{
    /* Create an autorelease NodeLoaderLibrary. */
    NodeLoaderLibrary * ccNodeLoaderLibrary = NodeLoaderLibrary::newDefaultNodeLoaderLibrary();

    ccNodeLoaderLibrary->registerNodeLoader("{ClassName}", {ClassName}Loader::loader());

    /* Create an autorelease CCBReader. */
    cocosbuilder::CCBReader * ccbReader = new cocosbuilder::CCBReader(ccNodeLoaderLibrary);
    ccbReader->setCCBRootPath("res/");
    auto node = ccbReader->readNodeGraphFromFile("res/{ccbiFile}");
    node->setPosition(Director::getInstance()->getWinSize()/2);
    
    CCBAnimationManager *ptr = dynamic_cast<CCBAnimationManager*>(node->getUserObject());

    {ClassName} *nodePtr = dynamic_cast<{ClassName}*>(node);
    nodePtr->setAnimManager(ptr);

    node->setUserObject(NULL);
    ccbReader->autorelease();

    return nodePtr;
}}

void {ClassName}::setState({ClassName}::UiState state)
{{
    if(_curState == state){{
        log("setState called with current state");
        return;
    }}

    if(pAnimManager == NULL){{
        log("AnimManager missing");
        return;
    }}

    _curState = state;
    pAnimManager->runAnimationsForSequenceIdTweenDuration(_curState, 0);
}}

void {ClassName}::setAnimManager(CCBAnimationManager *ptr)
{{
    CC_SAFE_RELEASE(pAnimManager);
    pAnimManager = ptr;
    CC_SAFE_RETAIN(pAnimManager);
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
    
    _curState = {ClassName}::UiState({DefaultAnimSequence});
    pAnimManager = NULL;
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

