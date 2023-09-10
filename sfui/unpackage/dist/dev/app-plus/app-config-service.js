
var isReady=false;var onReadyCallbacks=[];
var isServiceReady=false;var onServiceReadyCallbacks=[];
var __uniConfig = {"pages":["pages/MySpace/MySpace","pages/Paint/Paint","pages/Square/Square","pages/Register/Register","pages/Login/Login","pages/Info/Info","pages/showImg/showImg","pages/search/search","pages/inpaint/inpaint","pages/OtherSpace/OtherSpace"],"window":{"backgroundColor":"#f3f4f6","navigationBarBackgroundColor":"#FF5A5F","navigationBarTextStyle":"white"},"tabBar":{"list":[{"iconPath":"static/tabBar-icon/paint/paint.png","selectedIconPath":"static/tabBar-icon/paint/paint-a.png","text":"创作中心","pagePath":"pages/Paint/Paint"},{"iconPath":"static/tabBar-icon/square/square.png","selectedIconPath":"static/tabBar-icon/square/square-a.png","text":"梦图广场","pagePath":"pages/Square/Square"},{"iconPath":"static/tabBar-icon/space/space.png","selectedIconPath":"static/tabBar-icon/space/space-a.png","text":"个人中心","pagePath":"pages/MySpace/MySpace"}],"backgroundColor":"#ffffff","color":"#1b262c","selectedColor":"#FF5A5F","borderStyle":"#e3e4e5","fontSize":"15px","height":"60rpx"},"darkmode":false,"nvueCompiler":"uni-app","nvueStyleCompiler":"uni-app","renderer":"auto","splashscreen":{"alwaysShowBeforeRender":true,"autoclose":false},"appname":"sfui","compilerVersion":"3.8.7","entryPagePath":"pages/MySpace/MySpace","networkTimeout":{"request":60000,"connectSocket":60000,"uploadFile":60000,"downloadFile":60000}};
var __uniRoutes = [{"path":"/pages/MySpace/MySpace","meta":{"isQuit":true,"isTabBar":true},"window":{"navigationBarTitleText":"个人空间","navigationStyle":"custom","navigationBarTextStyle":"black"}},{"path":"/pages/Paint/Paint","meta":{"isQuit":true,"isTabBar":true},"window":{"navigationBarTitleText":"创作中心"}},{"path":"/pages/Square/Square","meta":{"isQuit":true,"isTabBar":true},"window":{"navigationBarTitleText":"梦图广场","navigationStyle":"custom","onReachBottomDistance":10,"enablePullDownRefresh":true,"navigationBarTextStyle":"black","pullToRefresh":{"color":"#FF5A5F"}}},{"path":"/pages/Register/Register","meta":{},"window":{"navigationBarTitleText":"注册","enablePullDownRefresh":false}},{"path":"/pages/Login/Login","meta":{},"window":{"navigationBarTitleText":"登录","enablePullDownRefresh":false}},{"path":"/pages/Info/Info","meta":{},"window":{"navigationBarTitleText":"个人空间","navigationStyle":"custom","enablePullDownRefresh":false,"navigationBarTextStyle":"black"}},{"path":"/pages/showImg/showImg","meta":{},"window":{"navigationBarTitleText":"图片详情","enablePullDownRefresh":true,"onReachBottomDistance":10,"pullToRefresh":{"color":"#FF5A5F"}}},{"path":"/pages/search/search","meta":{},"window":{"navigationBarTitleText":"搜索结果","enablePullDownRefresh":true,"onReachBottomDistance":5,"pullToRefresh":{"color":"#FF5A5F"}}},{"path":"/pages/inpaint/inpaint","meta":{},"window":{"navigationBarTitleText":"","enablePullDownRefresh":false}},{"path":"/pages/OtherSpace/OtherSpace","meta":{},"window":{"navigationStyle":"custom","enablePullDownRefresh":true,"navigationBarTextStyle":"black","pullToRefresh":{"color":"#FF5A5F"}}}];
__uniConfig.onReady=function(callback){if(__uniConfig.ready){callback()}else{onReadyCallbacks.push(callback)}};Object.defineProperty(__uniConfig,"ready",{get:function(){return isReady},set:function(val){isReady=val;if(!isReady){return}const callbacks=onReadyCallbacks.slice(0);onReadyCallbacks.length=0;callbacks.forEach(function(callback){callback()})}});
__uniConfig.onServiceReady=function(callback){if(__uniConfig.serviceReady){callback()}else{onServiceReadyCallbacks.push(callback)}};Object.defineProperty(__uniConfig,"serviceReady",{get:function(){return isServiceReady},set:function(val){isServiceReady=val;if(!isServiceReady){return}const callbacks=onServiceReadyCallbacks.slice(0);onServiceReadyCallbacks.length=0;callbacks.forEach(function(callback){callback()})}});
service.register("uni-app-config",{create(a,b,c){if(!__uniConfig.viewport){var d=b.weex.config.env.scale,e=b.weex.config.env.deviceWidth,f=Math.ceil(e/d);Object.assign(__uniConfig,{viewport:f,defaultFontSize:Math.round(f/20)})}return{instance:{__uniConfig:__uniConfig,__uniRoutes:__uniRoutes,global:void 0,window:void 0,document:void 0,frames:void 0,self:void 0,location:void 0,navigator:void 0,localStorage:void 0,history:void 0,Caches:void 0,screen:void 0,alert:void 0,confirm:void 0,prompt:void 0,fetch:void 0,XMLHttpRequest:void 0,WebSocket:void 0,webkit:void 0,print:void 0}}}});
