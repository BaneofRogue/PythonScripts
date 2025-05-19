(e, mqttService, r) => {
        "use strict";
        var n = r(564836);
        Object.defineProperty(mqttService, "__esModule", {
            value: !0
        }),
        mqttService.getMqttClient = mqttService.MQTTWebullClient = void 0;
        var a = n(r(670215))
          , i = n(r(310434))
          , o = n(r(856690))
          , l = n(r(689728))
          , subscriptionManager = n(r(238416))
          , s = r(206177)
          , c = r(693761)
          , d = n(r(848516))
          , f = n(r(917537))
          , p = n(r(229969))
          , h = n(r(365347))
          , g = r(290090)
          , v = r(536167)
          , marketDepthQueues = ["askBkQueue", "bidBkQueue", "askBkQueueExt", "bidBkQueueExt"];
        function y(e, t) {
            var r = "undefined" !== typeof Symbol && e[Symbol.iterator] || e["@@iterator"];
            if (!r) {
                if (Array.isArray(e) || (r = function(e, t) {
                    if (!e)
                        return;
                    if ("string" === typeof e)
                        return b(e, t);
                    var r = Object.prototype.toString.call(e).slice(8, -1);
                    "Object" === r && e.constructor && (r = e.constructor.name);
                    if ("Map" === r || "Set" === r)
                        return Array.from(e);
                    if ("Arguments" === r || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(r))
                        return b(e, t)
                }(e)) || t && e && "number" === typeof e.length) {
                    r && (e = r);
                    var n = 0
                      , a = function() {};
                    return {
                        s: a,
                        n: function() {
                            return n >= e.length ? {
                                done: !0
                            } : {
                                done: !1,
                                value: e[n++]
                            }
                        },
                        e: function(e) {
                            throw e
                        },
                        f: a
                    }
                }
                throw new TypeError("Invalid attempt to iterate non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
            }
            var i, o = !0, l = !1;
            return {
                s: function() {
                    r = r.call(e)
                },
                n: function() {
                    var e = r.next();
                    return o = e.done,
                    e
                },
                e: function(e) {
                    l = !0,
                    i = e
                },
                f: function() {
                    try {
                        o || null == r.return || r.return()
                    } finally {
                        if (l)
                            throw i
                    }
                }
            }
        }
        function b(e, t) {
            (null == t || t > e.length) && (t = e.length);
            for (var r = 0, n = new Array(t); r < t; r++)
                n[r] = e[r];
            return n
        }
        var MqttClient, _ = r(901306), w = "MQTTWebullClient => ", k = {
            host: s.domainSetting.PushUrl,
            port: s.domainSetting.PushPort,
            username: "test",
            password: "test",
            useSSL: s.domainSetting.PushSSL,
            messageType: "byte"
        }, MqttClientHandler = function() {
            function e() {
                var t = this;
                return (0,
                o.default)(this, e),
                (0,
                subscriptionManager.default)(this, "listeners", []),
                (0,
                subscriptionManager.default)(this, "subTypes", {}),
                (0,
                subscriptionManager.default)(this, "subItemRefs", {}),
                (0,
                subscriptionManager.default)(this, "hasDoConnect", !1),
                (0,
                subscriptionManager.default)(this, "doConnect", (function() {
                    t.connect()
                }
                )),
                (0,
                subscriptionManager.default)(this, "onConnect", (function() {
                    d.default.info(w, "onConnect, resubscribe");
                    var e = t.subTypes;
                    Object.keys(e).forEach((function(r) {
                        var n = e[r];
                        0 !== n.size && r.split("+").forEach((function(e) {
                            t.client.subscribe(JSON.stringify({
                                tickerIds: Array.from(n),
                                type: e,
                                flag: "1,50"
                            }))
                        }
                        ))
                    }
                    ))
                }
                )),
                (0,
                subscriptionManager.default)(this, "onMessageArrived", (function(e, r) {
                    var n, o;
                    try {
                        if (n = JSON.parse(e),
                        "1,50".includes(n.flag)) {
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
                            if (null !== T && void 0 !== T && T.inited && n.tickerId && n.type) {
                                var E = n
                                  , O = E.tickerId
                                  , C = E.type;
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
                                a.default)(f, marketDepthQueues);
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
                    } catch (K) {}
                    if (n && o) {
                        var U = n
                          , z = U.tickerId
                          , V = U.type;
                        t.streamSubscriber.push(Number(z), V.toString(), o)
                    }
                }
                )),
                (0,
                subscriptionManager.default)(this, "onTickerMessages", (function(e) {
                    var r, n = y(e);
                    try {
                        for (n.s(); !(r = n.n()).done; )
                            for (var a = r.value, i = a.type, o = a.tickerId, l = a.ticker, u = t.listeners, s = u.length, c = 0; c < s; ++c) {
                                var d = u[c]
                                  , f = d.tickerIds
                                  , p = d.types
                                  , h = d.callback;
                                p.includes(i) && -1 !== f.indexOf(o) && h(l)
                            }
                    } catch (g) {
                        n.e(g)
                    } finally {
                        n.f()
                    }
                }
                )),
                e.instance || (e.instance = this),
                (0,
                v.initSubscribeItemRefsDevTools)(e.instance),
                e.instance
            }
            return (0,
            l.default)(e, [{
                key: "connect",
                value: function() {
                    var e = this;
                    this.streamSubscriber = new h.default(this.onTickerMessages),
                    this.client = new p.default(window.appStore.stores,this.onMessageArrived,this.onConnect),
                    this.client.connect(k),
                    f.default.onDidSleep((function() {
                        d.default.info(w, "onDidSleep disconnect"),
                        e.client && e.client.destroy()
                    }
                    )),
                    f.default.onDidWakeUp((function() {
                        d.default.info(w, "onDidWakeUp connect"),
                        e.client && e.client.connect(k)
                    }
                    ))
                }
            }, {
                key: "subscribeTickers",
                value: function(e, t, r) {
                    var n = this;
                    if (0 !== e.length) {
                        if (this.hasDoConnect || (this.hasDoConnect = !0,
                        this.doConnect()),
                        this.subTypes[t]) {
                            var a = this.subTypes[t];
                            e.forEach((function(e) {
                                return a.add(e)
                            }
                            ))
                        } else
                            this.subTypes[t] = new Set(e);
                        var i = this.subItemRefs;
                        if (e.forEach((function(e) {
                            var r = "".concat(t, "&").concat(e);
                            i[r] = (i[r] || 0) + 1
                        }
                        )),
                        this.listeners.push({
                            tickerIds: e,
                            callback: r,
                            types: t.split("+")
                        }),
                        this.client.connected)
                            t.split("+").forEach((function(t) {
                                n.client.subscribe(JSON.stringify({
                                    tickerIds: e,
                                    type: t,
                                    flag: "1,50"
                                }))
                            }
                            ));
                        return {
                            dispose: function() {
                                var a = [];
                                e.forEach((function(e) {
                                    var r = "".concat(t, "&").concat(e)
                                      , o = i[r] - 1;
                                    i[r] = o,
                                    o <= 0 && (a.push(e),
                                    n.subTypes[t].delete(e))
                                }
                                ));
                                var o = (0,
                                c.findIndex)(n.listeners, (function(e) {
                                    return e.callback === r
                                }
                                ));
                                if (o > -1 && n.listeners.splice(o, 1),
                                0 !== a.length && n.client.connected) {
                                    var l = "[" + a.map((function(e) {
                                        return t.split("+").map((function(t) {
                                            return '"type='.concat(t, "&tid=").concat(e, '"')
                                        }
                                        ))
                                    }
                                    )).flat().join(",") + "]";
                                    n.client.unsubscribe(l)
                                }
                            }
                        }
                    }
                }
            }]),
            e
        }();
        mqttService.MQTTWebullClient = MqttClientHandler;
        mqttService.getMqttClient = function() {
            return MqttClient || (MqttClient = new MqttClientHandler),
            MqttClient
        }
    }