(0,
    u.default)(this, "onMessageArrived", (function (e, r) {
        var n, o;
        try {
            // Debug: print incoming message
            console.log("Raw message:", e);
            if (n = JSON.parse(e),
                "1,50".includes(n.flag)) {
                // Debug: print parsed message
                console.log("Parsed message:", n);

                var l = _.rpc.ItemsCombo.decode(r)
                    , u = l.base
                    , s = l.sale
                    , c = l.stats
                    , d = l.deal
                    , f = l.quote
                    , p = l.ntv
                    , h = l.quoteOne
                    , v = l.greeks
                    , y = l.nightPrice
                    , b = l.nightStats
                    , S = l.nightQuote
                    , w = l.nightDeal
                    , k = l.nightDepth
                    , T = l.alert;

                // Debug: print decoded data
                console.log("Decoded data:", l);

                if (null !== T && void 0 !== T && T.inited && n.tickerId && n.type) {
                    var E = n
                        , O = E.tickerId
                        , C = E.type;
                    // Debug: print alert info
                    console.log("Alert info:", T);
                    return void t.streamSubscriber.push(Number(O), C.toString(), T)
                }
                if (o = {},
                    null !== u && void 0 !== u && u.inited && (0,
                        i.default)(o, u),
                    null !== s && void 0 !== s && s.inited && (0,
                        i.default)(o, s),
                    null !== c && void 0 !== c && c.inited && (0,
                        i.default)(o, c),
                    null !== f && void 0 !== f && f.inited) {
                    var x = f.askBkQueue
                        , I = f.bidBkQueue
                        , P = f.askBkQueueExt
                        , A = f.bidBkQueueExt
                        , M = (0,
                            a.default)(f, m);
                    null !== x && void 0 !== x && x.length && (M.askBkQueue = x),
                        null !== I && void 0 !== I && I.length && (M.bidBkQueue = I),
                        null !== P && void 0 !== P && P.length && (M.askBkQueueExt = P),
                        null !== A && void 0 !== A && A.length && (M.bidBkQueueExt = A),
                        (0,
                            i.default)(o, M)
                }
                if ((null !== d && void 0 !== d && d.inited || null !== w && void 0 !== w && w.inited) && (0,
                    i.default)(o, {
                        deal: d || w
                    }),
                    p && (o.depth = p),
                    null !== v && void 0 !== v && v.inited && (0,
                        i.default)(o, v),
                    null !== h && void 0 !== h && h.inited && (o.quoteOne = h),
                    null !== y && void 0 !== y && y.init) {
                    var D = y.change
                        , N = y.changeRatio
                        , R = y.price;
                    (0,
                        i.default)(o, {
                            nChange: D,
                            nChangeRatio: N,
                            nPrice: R
                        })
                }
                if (null !== b && void 0 !== b && b.init) {
                    var L = b.tradeTime
                        , B = b.volume
                        , j = b.dealAmount
                        , F = b.high
                        , W = b.low;
                    (0,
                        i.default)(o, {
                            nVolume: B,
                            nDealAmount: j,
                            nTradeTime: L,
                            nHight: F,
                            nLow: W
                        })
                }
                if (null !== S && void 0 !== S && S.init) {
                    var G = S.askList
                        , H = S.bidList;
                    (0,
                        i.default)(o, {
                            nAskList: G,
                            nBidList: H
                        })
                }
                null !== k && void 0 !== k && k.inited && (o.nDepth = k)
            } else
                "string" !== typeof r && (r = (0,
                    g.parseUTF8)(r, 0, r.length)),
                    o = JSON.parse(r)
        } catch (K) {
            // Debug: print error
            console.error("Error in onMessageArrived:", K);
        }
        if (n && o) {
            var U = n
                , z = U.tickerId
                , V = U.type;
            // Debug: print final data to be pushed
            console.log("Push to streamSubscriber:", {
                tickerId: z,
                type: V,
                data: o
            });
            t.streamSubscriber.push(Number(z), V.toString(), o)
        }
    }
    ))