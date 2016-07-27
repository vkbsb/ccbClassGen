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
    public: 
    //enums for setting the state.
    enum UiState {{
        UiState_INVALID = -1,
        {AnimsEnum}
    }};

    private:
    //variables come here.
    {MemberVariables}

    {ClassName}::UiState _curState; 
    {ClassName}::UiState _prevState;
    CCBAnimationManager *pAnimManager;

    public:


    bool init();
    virtual void onEnter();
    virtual void onExit();

    virtual cocos2d::SEL_MenuHandler onResolveCCBCCMenuItemSelector(cocos2d::Ref * pTarget, const char* pSelectorName);
    virtual Control::Handler onResolveCCBCCControlSelector(cocos2d::Ref * pTarget, const char* pSelectorName);
    virtual bool onAssignCCBMemberVariable(cocos2d::Ref* target, const char* memberVariableName, cocos2d::Node* node);

    //animation related functions.
    void setAnimManager(CCBAnimationManager *ptr);
    void setState({ClassName}::UiState state);
    {ClassName}::UiState getCurState(){{ return _curState; }}
    {ClassName}::UiState getPrevState(){{ return _prevState; }}

    //member functions for callbacks.
    {ClassMethods}

    ~{ClassName}();
    CREATE_FUNC({ClassName});

    static Scene * createScene();
    static {ClassName}* getNewInstance();
}};

class {ClassName}Loader : public {BaseClass}Loader {{
    public:
        CCB_STATIC_NEW_AUTORELEASE_OBJECT_METHOD({ClassName}Loader, loader);

        CCB_VIRTUAL_NEW_AUTORELEASE_CREATECCNODE_METHOD({ClassName});
}};

#endif /* defined(__{ClassName}__) */ 

