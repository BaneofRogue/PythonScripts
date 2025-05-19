(e, constants, r) => {
        "use strict";
        Object.defineProperty(constants, "__esModule", {
            value: !0
        }),
        constants.tickerType = constants.regionSetting = constants.passwordRegNew = constants.passwordReg = constants.passwordNumReg = constants.passwordLetterReg = constants.numberReg = constants.newEmailReg = constants.maxSearchHistoryCount = constants.maxRecentTickersCount = constants.emailReg = constants.domainSetting = constants.defaultUserId = constants.defaultTickers = constants.defaultTickerInfos = constants.defaultPortfolioId = constants.defaultCurrency = constants.chinaPhoneReg = constants.cacheExpireTime = constants.TickerSubType = constants.TICKER_TYPE = constants.TICKER_STATUS = constants.TICKER_SHOW_TYPE = constants.TICKER_SEC_TYPE = constants.TICKER_LIST_STATUS = constants.TICKER_IPO_STATUS = constants.THEME_TYPE_STR = constants.THEME_TYPES = constants.TEMPLATE = constants.STOCKVIEW_TYPE = constants.SCREENERVIEW_TYPE = constants.RECENTVIEW_TYPE = constants.QRStatus = constants.PointBasedPrice = constants.OTCExchangeIds = constants.OTCExchangeCodes = constants.OPTION_TRADEVIEW_TYPE = constants.MESMAIN_TICKER = constants.MAX_MAIN_INDICATOR = constants.MAX_DUTY_INDICATOR = constants.MARKET_CHANNEL_TYPE = constants.MARKET_CHANNEL_BORD = constants.KEY_CODE = constants.INXExchangeId = constants.HSIExchangeId = constants.GOOGLE_TICKER = constants.FuturesContractType = constants.FaqId = constants.EXCHANGE_TYPE = constants.EXCHANGE_ID = constants.EXCHANGE_CODE = constants.DJIExchangeId = constants.CoinbaseExchangeCodes = constants.CURRENCY_USD = constants.COLOR_TYPES = constants.CODE_TYPE = constants.CODE_NAME_TYPES = constants.BigVersion = constants.ACCOUNT_TYPE = constants.AAPL_TICKER = constants.AAPLTickerId = void 0;
        var n = r(178794);
        constants.domainSetting = {
            ActApiDomain: "https://u1sact.webullfinance.com/",
            CsApiDomain: "https://u1scs.webullfinance.com/",
            NewQuoteDomain: "https://quotes-gw.webullfintech.com/",
            UserQuoteDomain: "https://quotes-gw.webullfintech.com/",
            NewUserDomain: "https://u1suser.webullfintech.com/",
            TradeUnitDomain: "https://trade.webullfintech.com/",
            UsTradeUnitDomain: "https://ustrade.webullfinance.com/",
            TradeHKDomain: "https://hktrade.wbsecurities.com/",
            PaperTradeDomain: "https://act.webullfintech.com/",
            PushUrl: "wspush.webullfintech.com",
            PushPort: 443,
            PushSSL: !0,
            PlatpushUrl: "platpush.webullfintech.com",
            PlatpushPort: 443,
            PlatSSL: !0,
            WebullAppDomain: "https://www.webullapp.com/",
            AccountDomain: "https://www.webull.com/",
            AccountHKDomain: "https://www.webull.hk/",
            GrpcDomain: "https://grpc-push.webullfinance.com",
            PaperTradeGrpcDomain: "https://paper-grpc-push.webullfintech.com",
            EventUrl: "https://data.webullfintech.com/event/json",
            ActDomain: "https://act.webull.com/",
            PspDomain: "https://sp.webull.com/",
            H5UserUrl: "https://passport.webull.com/",
            USFinUploadUrl: "https://u1supload.webullfinance.com/",
            USUploadUrl: "https://u1supload.webullfintech.com/",
            NaAppDomain: "https://naapp.webullfintech.com/",
            NaAppFileDomain: "https://u1sfile.webullfintech.com/",
            MsgApiDomain: "https://u1smsg.webullfintech.com/",
            CommunityDomain: "https://nacomm.webullfintech.com/",
            UsTradeUploadDomain: "https://ustrade-upload.webullfinance.com/",
            UsTradeUploadTempDomain: "https://ustrade.wb4magxg.com/",
            QuotesStaticDomain: "https://quotes-static.webullfintech.com",
            wealthDomain: "https://uswm.webullfinance.com/"
        };
        var regionIdentifiers = {
            CHINA: 1,
            HK: 2,
            US: 6,
            IN: 12,
            AU: 18,
            SG: 13,
            ZA: 159
        };
        constants.regionSetting = regionIdentifiers;
        constants.EXCHANGE_CODE = {
            HKG: "HKG",
            NSQ: "NSQ",
            NYSE: "NYSE"
        };
        constants.EXCHANGE_ID = {
            HKG: 3,
            NSQ: 96,
            NYSE: 11
        };
        var i = function(e) {
            return e.PHONE = "1",
            e.EMAIL = "2",
            e
        }({});
        constants.ACCOUNT_TYPE = i;
        var createActionTypeEnum = function(actionType) {
            return actionType[actionType.REGISTER = 1] = "REGISTER",
            actionType[actionType.RESET_PWD = 2] = "RESET_PWD",
            actionType[actionType.BIND_TYPE = 3] = "BIND_TYPE",
            actionType[actionType.UNBIND_TYPE = 4] = "UNBIND_TYPE",
            actionType[actionType.DEVICE_LOGIN = 5] = "DEVICE_LOGIN",
            actionType[actionType.BIND_NEW = 6] = "BIND_NEW",
            actionType
        }({});
        constants.CODE_TYPE = createActionTypeEnum;
        var initializeStatus = function(statusObject) {
            return statusObject.LOADING = "LOADING",
            statusObject.INVALID = "INVALID",
            statusObject.INIT = "INIT",
            statusObject.SCANNING = "SCANNING",
            statusObject.SCANNED = "SCANNED",
            statusObject
        }({});
        constants.QRStatus = initializeStatus;
        var initializeTradeStatus = function(tradeStatus) {
            return tradeStatus.WILL_OPEN = "W",
            tradeStatus.AUCTION = "C",
            tradeStatus.OPENING = "T",
            tradeStatus.PRE_TRADE = "F",
            tradeStatus.AFTER_TRADE = "A",
            tradeStatus.OVERNIGHT = "N",
            tradeStatus.NOON_CLOSED = "M",
            tradeStatus.CLOSED = "B",
            tradeStatus.HAS_CLOSED = "D",
            tradeStatus.NOT_OPEN = "H",
            tradeStatus.SUSPENSION = "P",
            tradeStatus
        }({});
        constants.TICKER_STATUS = initializeTradeStatus;
        var initializeTransactionStates = function(transactionStates) {
            return transactionStates[transactionStates.DE = 3] = "DE",
            transactionStates[transactionStates.UN = 4] = "UN",
            transactionStates[transactionStates.TO = 5] = "TO",
            transactionStates[transactionStates.DELAY = 6] = "DELAY",
            transactionStates[transactionStates.WITHDRAW = 7] = "WITHDRAW",
            transactionStates
        }({});
        constants.TICKER_IPO_STATUS = initializeTransactionStates;
        var initializeIpoStates = function(ipoTransactionStates) {
            return ipoTransactionStates[ipoTransactionStates.L = 1] = "L",
            ipoTransactionStates[ipoTransactionStates.DE = 3] = "DE",
            ipoTransactionStates[ipoTransactionStates.UN = 4] = "UN",
            ipoTransactionStates[ipoTransactionStates.TO = 5] = "TO",
            ipoTransactionStates[ipoTransactionStates.DELAY = 6] = "DELAY",
            ipoTransactionStates[ipoTransactionStates.WITHDRAW = 7] = "WITHDRAW",
            ipoTransactionStates
        }({});
        constants.TICKER_LIST_STATUS = initializeIpoStates;
        constants.tickerType = {
            1: "indice",
            2: "stock",
            3: "fund",
            4: "futures",
            6: "exchange",
            7: "indexFutures",
            8: "stockFutures",
            9: "indexOptions",
            10: "stockOptions",
            16: "bond"
        };
        var d = function(assetTypes) {
            return assetTypes.STOCK = "stock",
            assetTypes.INDICE = "index",
            assetTypes.ETF = "etf",
            assetTypes.MMF = "mutf_trade_fh",
            assetTypes.MUTF = "mutf",
            assetTypes.FOREX = "forex",
            assetTypes.FUT = "fut",
            assetTypes.FUTEOD = "futEod",
            assetTypes.IDXFUT = "idxFut",
            assetTypes.IDXFUTEOD = "idxFutEod",
            assetTypes.IPO = "ipo",
            assetTypes.PREIPO = "preIpo",
            assetTypes.CRYPTO = "crypto",
            assetTypes.CRYPTOASSET = "crypto_asset",
            assetTypes.WARRANT = "warrant",
            assetTypes.CBBC = "cbbc",
            assetTypes.INLINEWT = "inlinewt",
            assetTypes.DERIVATIVE = "derivative",
            assetTypes.OPTION = "option",
            assetTypes.BOND = "bond",
            assetTypes
        }({});
        constants.TEMPLATE = d;
        var f = function(e) {
            return e[e.INDICE = 1] = "INDICE",
            e[e.STOCK = 2] = "STOCK",
            e[e.FUND = 3] = "FUND",
            e[e.FUTURES = 13] = "FUTURES",
            e[e.OLDFUTURES = 4] = "OLDFUTURES",
            e[e.EXCHANGE = 6] = "EXCHANGE",
            e[e.OPTION = 7] = "OPTION",
            e[e.CRYPTO = 8] = "CRYPTO",
            e[e.WARRANT = 9] = "WARRANT",
            e[e.BOND = 16] = "BOND",
            e.StockAndETF = "StockAndETF",
            e
        }({});
        constants.TICKER_TYPE = f;
        var p = function(e) {
            return e[e.bondYield = 1607] = "bondYield",
            e
        }({});
        constants.TickerSubType = p;
        var h = function(e) {
            return e[e.ETF = 34] = "ETF",
            e
        }({});
        constants.TICKER_SEC_TYPE = h;
        var g = function(e) {
            return e[e.FX = 0] = "FX",
            e[e.CRYPTO = 1] = "CRYPTO",
            e
        }({});
        constants.EXCHANGE_TYPE = g;
        var v = function(e) {
            return e[e.STOCK = "".concat(d.STOCK)] = "STOCK",
            e[e.STOCK_US = "".concat(d.STOCK, "-").concat(regionIdentifiers.US)] = "STOCK_US",
            e[e.INDICE = "".concat(d.INDICE)] = "INDICE",
            e[e.FUTURES = "".concat(d.FUT)] = "FUTURES",
            e[e.EXCHANGE_FX = "".concat(d.FOREX, "-").concat(g.FX)] = "EXCHANGE_FX",
            e[e.EXCHANGE_CRYPTO = "".concat(d.FOREX, "-").concat(g.CRYPTO)] = "EXCHANGE_CRYPTO",
            e[e.FUND_ETF = "".concat(d.ETF)] = "FUND_ETF",
            e[e.FUND_ETF_US = "".concat(d.ETF, "-").concat(regionIdentifiers.US)] = "FUND_ETF_US",
            e[e.FUND_MMF = "".concat(d.MMF)] = "FUND_MMF",
            e[e.FUND_MUTUAL = "".concat(d.MUTF)] = "FUND_MUTUAL",
            e[e.OPTION = "".concat(d.OPTION)] = "OPTION",
            e[e.BOND = "".concat(d.BOND)] = "BOND",
            e[e.DEFAULT = "default"] = "DEFAULT",
            e
        }({});
        constants.TICKER_SHOW_TYPE = v;
        var m = 913256135;
        constants.AAPLTickerId = m;
        var y = {
            tickerId: 913256135,
            template: d.STOCK,
            type: f.STOCK
        };
        constants.AAPL_TICKER = y;
        var b = {
            tickerId: 470005101,
            template: d.FUT,
            type: f.FUTURES
        };
        constants.MESMAIN_TICKER = b;
        var S = {
            tickerId: 913303964,
            template: d.STOCK,
            type: f.STOCK
        };
        constants.GOOGLE_TICKER = S;
        constants.INXExchangeId = 53;
        constants.DJIExchangeId = 54;
        constants.HSIExchangeId = 87;
        constants.OTCExchangeIds = [112, 200, 201, 202, 203, 204, 205];
        constants.OTCExchangeCodes = ["PK", "PTCQ", "OTCB", "PINC", "PINL", "EXPM", "PSGM"];
        constants.CoinbaseExchangeCodes = ["CDE"];
        var _ = [913354090, 913243250, 913354362, m, 913303964];
        constants.defaultTickers = _;
        var w = [{
            tickerId: 913354090,
            template: d.INDICE,
            type: f.INDICE
        }, {
            tickerId: 913243250,
            template: d.ETF,
            type: f.FUND
        }, {
            tickerId: 913354362,
            template: d.INDICE,
            type: f.INDICE
        }, y, S];
        constants.defaultTickerInfos = w;
        constants.defaultCurrency = ["USD", "INR", "EUR", "GBP", "HKD", "AUD", "CAD", "CNY", "JPY", "CHF", "AED", "ARS", "BRL", "DKK", "IDR", "ILS", "ISK", "KHR", "KRW", "MXN", "MYR", "PHP", "PKR", "RUB", "SEK", "SGD", "THB", "TRY", "TWD", "VND", "ZAR"];
        constants.defaultUserId = "default";
        constants.defaultPortfolioId = "-1";
        var k = function(e) {
            return e[e.RedUpGreenDown = 1] = "RedUpGreenDown",
            e[e.GreenUpRedDown = 2] = "GreenUpRedDown",
            e[e.GreenUpYellowDown = 3] = "GreenUpYellowDown",
            e
        }({});
        constants.COLOR_TYPES = k;
        var T = function(e) {
            return e[e.DARK = 1] = "DARK",
            e[e.LIGHT = 2] = "LIGHT",
            e
        }({});
        constants.THEME_TYPES = T;
        var E = function(e) {
            return e.DARK = "dark",
            e.LIGHT = "light",
            e
        }({});
        constants.THEME_TYPE_STR = E;
        var O = function(e) {
            return e[e.NAME_CODE = 1] = "NAME_CODE",
            e[e.CODE_NAME = 2] = "CODE_NAME",
            e
        }({});
        constants.CODE_NAME_TYPES = O;
        var C = {
            tickerRT: 3e3,
            tickerInfo: n.ONE_DAY,
            tickerMI_m1: n.ONE_MINUTE,
            tickerMI_m5: n.ONE_MINUTE,
            tickerTrend_m1: n.ONE_DAY,
            tickerTrend_m3: n.ONE_DAY,
            tickerTrend_m6: n.ONE_DAY,
            tickerTrend_y1: n.ONE_DAY,
            tickerTrend_y5: n.ONE_DAY,
            tickerTrend_all: n.ONE_DAY,
            tickerK_m1: n.ONE_MINUTE,
            tickerK_m5: n.ONE_MINUTE,
            tickerK_m15: n.ONE_MINUTE,
            tickerK_m30: n.ONE_MINUTE,
            tickerK_m60: n.ONE_MINUTE,
            tickerK_m120: n.ONE_MINUTE,
            tickerK_m240: n.ONE_MINUTE,
            tickerK_d1: n.ONE_DAY,
            tickerK_w1: n.ONE_DAY,
            tickerK_mth1: n.ONE_DAY,
            tickerK_mth3: n.ONE_DAY,
            tickerK_y1: n.ONE_DAY,
            tickerNews: n.ONE_HOUR,
            tickerBulletins: n.ONE_HOUR,
            marketChannel: n.ONE_WEEK,
            marketCategories: n.HALF_MINUTE,
            marketPageCardTickers: n.HALF_MINUTE
        };
        constants.cacheExpireTime = C;
        constants.maxSearchHistoryCount = 50;
        constants.maxRecentTickersCount = 50;
        var x = function(e) {
            return e[e.BACKSPACE = 8] = "BACKSPACE",
            e[e.DEL = 46] = "DEL",
            e[e.ESCAPE = 27] = "ESCAPE",
            e[e.ENTER = 13] = "ENTER",
            e[e.SHIFT = 16] = "SHIFT",
            e[e.CRL = 17] = "CRL",
            e[e.ALT = 18] = "ALT",
            e[e.LEFT = 37] = "LEFT",
            e[e.UP = 38] = "UP",
            e[e.RIGHT = 39] = "RIGHT",
            e[e.DOWN = 40] = "DOWN",
            e[e.F5 = 116] = "F5",
            e[e.F10 = 121] = "F10",
            e
        }({});
        constants.KEY_CODE = x;
        var I = function(e) {
            return e[e.WATCHLIST = 0] = "WATCHLIST",
            e[e.RECENTLIST = 1] = "RECENTLIST",
            e
        }({});
        constants.STOCKVIEW_TYPE = I;
        var P = function(e) {
            return e[e.WATCHLIST = 0] = "WATCHLIST",
            e[e.RECENTLIST = 1] = "RECENTLIST",
            e[e.TOPRANKING = 2] = "TOPRANKING",
            e
        }({});
        constants.OPTION_TRADEVIEW_TYPE = P;
        var A = function(e) {
            return e[e.RECENT = 0] = "RECENT",
            e[e.BORD = 1] = "BORD",
            e
        }({});
        constants.RECENTVIEW_TYPE = A;
        var M = function(e) {
            return e[e.SELECTLIST = 1] = "SELECTLIST",
            e[e.SCREENERLIST = 2] = "SCREENERLIST",
            e[e.OPTIONSELECTLIST = 3] = "OPTIONSELECTLIST",
            e[e.BONDSELECTLIST = 4] = "BONDSELECTLIST",
            e
        }({});
        constants.SCREENERVIEW_TYPE = M;
        var D = function(e) {
            return e[e.BORD = 1] = "BORD",
            e[e.REGION = 2] = "REGION",
            e
        }({});
        constants.MARKET_CHANNEL_TYPE = D;
        var N = function(e) {
            return e[e.ETF = 2] = "ETF",
            e[e.FOREX = 3] = "FOREX",
            e[e.COMMODITY = 4] = "COMMODITY",
            e[e.GLOBAL = 5] = "GLOBAL",
            e[e.FUND = 6] = "FUND",
            e[e.DIGITAL = 33] = "DIGITAL",
            e
        }({});
        constants.MARKET_CHANNEL_BORD = N;
        constants.MAX_DUTY_INDICATOR = 6;
        constants.MAX_MAIN_INDICATOR = 4;
        constants.CURRENCY_USD = 247;
        constants.emailReg = /^([a-zA-Z0-9_.-])+@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        constants.newEmailReg = /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/;
        constants.numberReg = /^\d+$/;
        constants.chinaPhoneReg = /^1\d{10}$/;
        constants.passwordReg = /^(?!([a-zA-Z]+|\d+)$)[\u0020-\u007F]+$/;
        constants.passwordNumReg = /^(?=.*\d)[^]{1,}$/;
        constants.passwordLetterReg = /^(?=.*[a-z])(?=.*[A-Z])[^]{1,}$/;
        constants.passwordRegNew = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^]{8,20}$/;
        var R = function(e) {
            return e[e.duotrigesimal = 1] = "duotrigesimal",
            e[e.octal = 2] = "octal",
            e[e.decimal = 3] = "decimal",
            e
        }({});
        constants.PointBasedPrice = R;
        var L = function(e) {
            return e[e.Month = 1] = "Month",
            e[e.MainContinuous = 2] = "MainContinuous",
            e[e.MonthContinuous = 3] = "MonthContinuous",
            e
        }({});
        constants.FuturesContractType = L;
        constants.BigVersion = "5.0";
        constants.FaqId = {
            TC: "10690-Technical-Summary-Scores"
        }
    };