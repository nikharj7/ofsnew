/** @license React v17.0.2
 * react.production.min.js
 *
 * Copyright (c) Facebook, Inc. and its affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
!(function () {
  "use strict";
  var e, t;
  (e = this),
    (t = function (e) {
      function t(e) {
        for (
          var t = "https://reactjs.org/docs/error-decoder.html?invariant=" + e,
            n = 1;
          n < arguments.length;
          n++
        )
          t += "&args[]=" + encodeURIComponent(arguments[n]);
        return (
          "Minified React error #" +
          e +
          "; visit " +
          t +
          " for the full message or use the non-minified dev environment for full errors and additional helpful warnings."
        );
      }
      function n(e, t, n) {
        (this.props = e),
          (this.context = t),
          (this.refs = E),
          (this.updater = n || $);
      }
      function r() {}
      function o(e, t, n) {
        (this.props = e),
          (this.context = t),
          (this.refs = E),
          (this.updater = n || $);
      }
      function u(e, t, n) {
        var r,
          o = {},
          u = null,
          i = null;
        if (null != t)
          for (r in (void 0 !== t.ref && (i = t.ref),
          void 0 !== t.key && (u = "" + t.key),
          t))
            M.call(t, r) && !A.hasOwnProperty(r) && (o[r] = t[r]);
        var a = arguments.length - 2;
        if (1 === a) o.children = n;
        else if (1 < a) {
          for (var l = Array(a), c = 0; c < a; c++) l[c] = arguments[c + 2];
          o.children = l;
        }
        if (e && e.defaultProps)
          for (r in (a = e.defaultProps)) void 0 === o[r] && (o[r] = a[r]);
        return {
          $$typeof: m,
          type: e,
          key: u,
          ref: i,
          props: o,
          _owner: I.current,
        };
      }
      function i(e) {
        return "object" == typeof e && null !== e && e.$$typeof === m;
      }
      function a(e, t) {
        return "object" == typeof e && null !== e && null != e.key
          ? (function (e) {
              var t = { "=": "=0", ":": "=2" };
              return (
                "$" +
                e.replace(/[=:]/g, function (e) {
                  return t[e];
                })
              );
            })("" + e.key)
          : t.toString(36);
      }
      function l(e, n, r, o, u) {
        var c = typeof e;
        ("undefined" !== c && "boolean" !== c) || (e = null);
        var f = !1;
        if (null === e) f = !0;
        else
          switch (c) {
            case "string":
            case "number":
              f = !0;
              break;
            case "object":
              switch (e.$$typeof) {
                case m:
                case w:
                  f = !0;
              }
          }
        if (f)
          return (
            (u = u((f = e))),
            (e = "" === o ? "." + a(f, 0) : o),
            Array.isArray(u)
              ? ((r = ""),
                null != e && (r = e.replace(F, "$&/") + "/"),
                l(u, n, r, "", function (e) {
                  return e;
                }))
              : null != u &&
                (i(u) &&
                  (u = (function (e, t) {
                    return {
                      $$typeof: m,
                      type: e.type,
                      key: t,
                      ref: e.ref,
                      props: e.props,
                      _owner: e._owner,
                    };
                  })(
                    u,
                    r +
                      (!u.key || (f && f.key === u.key)
                        ? ""
                        : ("" + u.key).replace(F, "$&/") + "/") +
                      e
                  )),
                n.push(u)),
            1
          );
        if (((f = 0), (o = "" === o ? "." : o + ":"), Array.isArray(e)))
          for (var s = 0; s < e.length; s++) {
            var p = o + a((c = e[s]), s);
            f += l(c, n, r, p, u);
          }
        else if (
          ((p = (function (e) {
            return null === e || "object" != typeof e
              ? null
              : "function" == typeof (e = (j && e[j]) || e["@@iterator"])
              ? e
              : null;
          })(e)),
          "function" == typeof p)
        )
          for (e = p.call(e), s = 0; !(c = e.next()).done; )
            f += l((c = c.value), n, r, (p = o + a(c, s++)), u);
        else if ("object" === c)
          throw (
            ((n = "" + e),
            Error(
              t(
                31,
                "[object Object]" === n
                  ? "object with keys {" + Object.keys(e).join(", ") + "}"
                  : n
              )
            ))
          );
        return f;
      }
      function c(e, t, n) {
        if (null == e) return e;
        var r = [],
          o = 0;
        return (
          l(e, r, "", "", function (e) {
            return t.call(n, e, o++);
          }),
          r
        );
      }
      function f(e) {
        if (-1 === e._status) {
          var t = e._result;
          (t = t()),
            (e._status = 0),
            (e._result = t),
            t.then(
              function (t) {
                0 === e._status &&
                  ((t = t.default), (e._status = 1), (e._result = t));
              },
              function (t) {
                0 === e._status && ((e._status = 2), (e._result = t));
              }
            );
        }
        if (1 === e._status) return e._result;
        throw e._result;
      }
      function s() {
        var e = L.current;
        if (null === e) throw Error(t(321));
        return e;
      }
      function p(e, t) {
        var n = e.length;
        e.push(t);
        e: for (;;) {
          var r = (n - 1) >>> 1,
            o = e[r];
          if (!(void 0 !== o && 0 < b(o, t))) break e;
          (e[r] = t), (e[n] = o), (n = r);
        }
      }
      function y(e) {
        return void 0 === (e = e[0]) ? null : e;
      }
      function d(e) {
        var t = e[0];
        if (void 0 !== t) {
          var n = e.pop();
          if (n !== t) {
            e[0] = n;
            e: for (var r = 0, o = e.length; r < o; ) {
              var u = 2 * (r + 1) - 1,
                i = e[u],
                a = u + 1,
                l = e[a];
              if (void 0 !== i && 0 > b(i, n))
                void 0 !== l && 0 > b(l, i)
                  ? ((e[r] = l), (e[a] = n), (r = a))
                  : ((e[r] = i), (e[u] = n), (r = u));
              else {
                if (!(void 0 !== l && 0 > b(l, n))) break e;
                (e[r] = l), (e[a] = n), (r = a);
              }
            }
          }
          return t;
        }
        return null;
      }
      function b(e, t) {
        var n = e.sortIndex - t.sortIndex;
        return 0 !== n ? n : e.id - t.id;
      }
      function v(e) {
        for (var t = y(ue); null !== t; ) {
          if (null === t.callback) d(ue);
          else {
            if (!(t.startTime <= e)) break;
            d(ue), (t.sortIndex = t.expirationTime), p(oe, t);
          }
          t = y(ue);
        }
      }
      function _(e) {
        if (((se = !1), v(e), !fe))
          if (null !== y(oe)) (fe = !0), H(h);
          else {
            var t = y(ue);
            null !== t && W(_, t.startTime - e);
          }
      }
      function h(e, t) {
        (fe = !1), se && ((se = !1), Y()), (ce = !0);
        var n = le;
        try {
          for (
            v(t), ae = y(oe);
            null !== ae && (!(ae.expirationTime > t) || (e && !G()));

          ) {
            var r = ae.callback;
            if ("function" == typeof r) {
              (ae.callback = null), (le = ae.priorityLevel);
              var o = r(ae.expirationTime <= t);
              (t = U()),
                "function" == typeof o
                  ? (ae.callback = o)
                  : ae === y(oe) && d(oe),
                v(t);
            } else d(oe);
            ae = y(oe);
          }
          if (null !== ae) var u = !0;
          else {
            var i = y(ue);
            null !== i && W(_, i.startTime - t), (u = !1);
          }
          return u;
        } finally {
          (ae = null), (le = n), (ce = !1);
        }
      }
      var m = 60103,
        w = 60106;
      (e.Fragment = 60107), (e.StrictMode = 60108), (e.Profiler = 60114);
      var g = 60109,
        k = 60110,
        C = 60112;
      e.Suspense = 60113;
      var S = 60115,
        x = 60116;
      if ("function" == typeof Symbol && Symbol.for) {
        var R = Symbol.for;
        (m = R("react.element")),
          (w = R("react.portal")),
          (e.Fragment = R("react.fragment")),
          (e.StrictMode = R("react.strict_mode")),
          (e.Profiler = R("react.profiler")),
          (g = R("react.provider")),
          (k = R("react.context")),
          (C = R("react.forward_ref")),
          (e.Suspense = R("react.suspense")),
          (S = R("react.memo")),
          (x = R("react.lazy"));
      }
      var j = "function" == typeof Symbol && Symbol.iterator,
        P = Object.prototype.hasOwnProperty,
        T =
          Object.assign ||
          function (e, t) {
            if (null == e)
              throw new TypeError(
                "Object.assign target cannot be null or undefined"
              );
            for (var n = Object(e), r = 1; r < arguments.length; r++) {
              var o = arguments[r];
              if (null != o) {
                var u = void 0;
                for (u in (o = Object(o))) P.call(o, u) && (n[u] = o[u]);
              }
            }
            return n;
          },
        $ = {
          isMounted: function (e) {
            return !1;
          },
          enqueueForceUpdate: function (e, t, n) {},
          enqueueReplaceState: function (e, t, n, r) {},
          enqueueSetState: function (e, t, n, r) {},
        },
        E = {};
      (n.prototype.isReactComponent = {}),
        (n.prototype.setState = function (e, n) {
          if ("object" != typeof e && "function" != typeof e && null != e)
            throw Error(t(85));
          this.updater.enqueueSetState(this, e, n, "setState");
        }),
        (n.prototype.forceUpdate = function (e) {
          this.updater.enqueueForceUpdate(this, e, "forceUpdate");
        }),
        (r.prototype = n.prototype),
        ((R = o.prototype = new r()).constructor = o),
        T(R, n.prototype),
        (R.isPureReactComponent = !0);
      var O,
        I = { current: null },
        M = Object.prototype.hasOwnProperty,
        A = { key: !0, ref: !0, __self: !0, __source: !0 },
        F = /\/+/g,
        L = { current: null };
      if (
        "object" == typeof performance &&
        "function" == typeof performance.now
      )
        var q = performance,
          U = function () {
            return q.now();
          };
      else {
        var D = Date,
          N = D.now();
        U = function () {
          return D.now() - N;
        };
      }
      if ("undefined" == typeof window || "function" != typeof MessageChannel) {
        var B = null,
          V = null,
          z = function () {
            if (null !== B)
              try {
                var e = U();
                B(!0, e), (B = null);
              } catch (e) {
                throw (setTimeout(z, 0), e);
              }
          },
          H = function (e) {
            null !== B ? setTimeout(H, 0, e) : ((B = e), setTimeout(z, 0));
          },
          W = function (e, t) {
            V = setTimeout(e, t);
          },
          Y = function () {
            clearTimeout(V);
          },
          G = function () {
            return !1;
          };
        R = O = function () {};
      } else {
        var J = window.setTimeout,
          K = window.clearTimeout;
        "undefined" != typeof console &&
          ((R = window.cancelAnimationFrame),
          "function" != typeof window.requestAnimationFrame &&
            console.error(
              "This browser doesn't support requestAnimationFrame. Make sure that you load a polyfill in older browsers. https://reactjs.org/link/react-polyfills"
            ),
          "function" != typeof R &&
            console.error(
              "This browser doesn't support cancelAnimationFrame. Make sure that you load a polyfill in older browsers. https://reactjs.org/link/react-polyfills"
            ));
        var Q = !1,
          X = null,
          Z = -1,
          ee = 5,
          te = 0;
        (G = function () {
          return U() >= te;
        }),
          (R = function () {}),
          (O = function (e) {
            0 > e || 125 < e
              ? console.error(
                  "forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"
                )
              : (ee = 0 < e ? Math.floor(1e3 / e) : 5);
          });
        var ne = new MessageChannel(),
          re = ne.port2;
        (ne.port1.onmessage = function () {
          if (null !== X) {
            var e = U();
            te = e + ee;
            try {
              X(!0, e) ? re.postMessage(null) : ((Q = !1), (X = null));
            } catch (e) {
              throw (re.postMessage(null), e);
            }
          } else Q = !1;
        }),
          (H = function (e) {
            (X = e), Q || ((Q = !0), re.postMessage(null));
          }),
          (W = function (e, t) {
            Z = J(function () {
              e(U());
            }, t);
          }),
          (Y = function () {
            K(Z), (Z = -1);
          });
      }
      var oe = [],
        ue = [],
        ie = 1,
        ae = null,
        le = 3,
        ce = !1,
        fe = !1,
        se = !1,
        pe = 0;
      (R = {
        ReactCurrentDispatcher: L,
        ReactCurrentOwner: I,
        IsSomeRendererActing: { current: !1 },
        ReactCurrentBatchConfig: { transition: 0 },
        assign: T,
        Scheduler: {
          __proto__: null,
          unstable_ImmediatePriority: 1,
          unstable_UserBlockingPriority: 2,
          unstable_NormalPriority: 3,
          unstable_IdlePriority: 5,
          unstable_LowPriority: 4,
          unstable_runWithPriority: function (e, t) {
            switch (e) {
              case 1:
              case 2:
              case 3:
              case 4:
              case 5:
                break;
              default:
                e = 3;
            }
            var n = le;
            le = e;
            try {
              return t();
            } finally {
              le = n;
            }
          },
          unstable_next: function (e) {
            switch (le) {
              case 1:
              case 2:
              case 3:
                var t = 3;
                break;
              default:
                t = le;
            }
            var n = le;
            le = t;
            try {
              return e();
            } finally {
              le = n;
            }
          },
          unstable_scheduleCallback: function (e, t, n) {
            var r = U();
            switch (
              ((n =
                "object" == typeof n &&
                null !== n &&
                "number" == typeof (n = n.delay) &&
                0 < n
                  ? r + n
                  : r),
              e)
            ) {
              case 1:
                var o = -1;
                break;
              case 2:
                o = 250;
                break;
              case 5:
                o = 1073741823;
                break;
              case 4:
                o = 1e4;
                break;
              default:
                o = 5e3;
            }
            return (
              (e = {
                id: ie++,
                callback: t,
                priorityLevel: e,
                startTime: n,
                expirationTime: (o = n + o),
                sortIndex: -1,
              }),
              n > r
                ? ((e.sortIndex = n),
                  p(ue, e),
                  null === y(oe) &&
                    e === y(ue) &&
                    (se ? Y() : (se = !0), W(_, n - r)))
                : ((e.sortIndex = o), p(oe, e), fe || ce || ((fe = !0), H(h))),
              e
            );
          },
          unstable_cancelCallback: function (e) {
            e.callback = null;
          },
          unstable_wrapCallback: function (e) {
            var t = le;
            return function () {
              var n = le;
              le = t;
              try {
                return e.apply(this, arguments);
              } finally {
                le = n;
              }
            };
          },
          unstable_getCurrentPriorityLevel: function () {
            return le;
          },
          get unstable_shouldYield() {
            return G;
          },
          unstable_requestPaint: R,
          unstable_continueExecution: function () {
            fe || ce || ((fe = !0), H(h));
          },
          unstable_pauseExecution: function () {},
          unstable_getFirstCallbackNode: function () {
            return y(oe);
          },
          get unstable_now() {
            return U;
          },
          get unstable_forceFrameRate() {
            return O;
          },
          unstable_Profiling: null,
        },
        SchedulerTracing: {
          __proto__: null,
          __interactionsRef: null,
          __subscriberRef: null,
          unstable_clear: function (e) {
            return e();
          },
          unstable_getCurrent: function () {
            return null;
          },
          unstable_getThreadID: function () {
            return ++pe;
          },
          unstable_trace: function (e, t, n) {
            return n();
          },
          unstable_wrap: function (e) {
            return e;
          },
          unstable_subscribe: function (e) {},
          unstable_unsubscribe: function (e) {},
        },
      }),
        (e.Children = {
          map: c,
          forEach: function (e, t, n) {
            c(
              e,
              function () {
                t.apply(this, arguments);
              },
              n
            );
          },
          count: function (e) {
            var t = 0;
            return (
              c(e, function () {
                t++;
              }),
              t
            );
          },
          toArray: function (e) {
            return (
              c(e, function (e) {
                return e;
              }) || []
            );
          },
          only: function (e) {
            if (!i(e)) throw Error(t(143));
            return e;
          },
        }),
        (e.Component = n),
        (e.PureComponent = o),
        (e.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED = R),
        (e.cloneElement = function (e, n, r) {
          if (null == e) throw Error(t(267, e));
          var o = T({}, e.props),
            u = e.key,
            i = e.ref,
            a = e._owner;
          if (null != n) {
            if (
              (void 0 !== n.ref && ((i = n.ref), (a = I.current)),
              void 0 !== n.key && (u = "" + n.key),
              e.type && e.type.defaultProps)
            )
              var l = e.type.defaultProps;
            for (c in n)
              M.call(n, c) &&
                !A.hasOwnProperty(c) &&
                (o[c] = void 0 === n[c] && void 0 !== l ? l[c] : n[c]);
          }
          var c = arguments.length - 2;
          if (1 === c) o.children = r;
          else if (1 < c) {
            l = Array(c);
            for (var f = 0; f < c; f++) l[f] = arguments[f + 2];
            o.children = l;
          }
          return {
            $$typeof: m,
            type: e.type,
            key: u,
            ref: i,
            props: o,
            _owner: a,
          };
        }),
        (e.createContext = function (e, t) {
          return (
            void 0 === t && (t = null),
            ((e = {
              $$typeof: k,
              _calculateChangedBits: t,
              _currentValue: e,
              _currentValue2: e,
              _threadCount: 0,
              Provider: null,
              Consumer: null,
            }).Provider = { $$typeof: g, _context: e }),
            (e.Consumer = e)
          );
        }),
        (e.createElement = u),
        (e.createFactory = function (e) {
          var t = u.bind(null, e);
          return (t.type = e), t;
        }),
        (e.createRef = function () {
          return { current: null };
        }),
        (e.forwardRef = function (e) {
          return { $$typeof: C, render: e };
        }),
        (e.isValidElement = i),
        (e.lazy = function (e) {
          return {
            $$typeof: x,
            _payload: { _status: -1, _result: e },
            _init: f,
          };
        }),
        (e.memo = function (e, t) {
          return { $$typeof: S, type: e, compare: void 0 === t ? null : t };
        }),
        (e.useCallback = function (e, t) {
          return s().useCallback(e, t);
        }),
        (e.useContext = function (e, t) {
          return s().useContext(e, t);
        }),
        (e.useDebugValue = function (e, t) {}),
        (e.useEffect = function (e, t) {
          return s().useEffect(e, t);
        }),
        (e.useImperativeHandle = function (e, t, n) {
          return s().useImperativeHandle(e, t, n);
        }),
        (e.useLayoutEffect = function (e, t) {
          return s().useLayoutEffect(e, t);
        }),
        (e.useMemo = function (e, t) {
          return s().useMemo(e, t);
        }),
        (e.useReducer = function (e, t, n) {
          return s().useReducer(e, t, n);
        }),
        (e.useRef = function (e) {
          return s().useRef(e);
        }),
        (e.useState = function (e) {
          return s().useState(e);
        }),
        (e.version = "17.0.2");
    }),
    "object" == typeof exports && "undefined" != typeof module
      ? t(exports)
      : "function" == typeof define && define.amd
      ? define(["exports"], t)
      : t(((e = e || self).React = {}));
})();
