import {
  useEffect,
  useContext,
} from "react";

import {
  PipelineContext,
} from "../context/PipelineContext";

/* ==========================================
   WEBSOCKET HOOK

   Frontend Owner:
   Ayushman (P3)

   Backend Owner:
   Animesh (P4)

   Endpoint:
   ws://localhost:8000/ws/pipeline

   Receives:

   {
     stage:
       "capture" |
       "preprocess" |
       "error_correct" |
       "hash" |
       "wipe" |
       "verify",

     status:
       "start" |
       "done" |
       "error",

     data:{}
   }
========================================== */

export default function useWebSocket() {

  const { dispatch } =
    useContext(
      PipelineContext
    );

  useEffect(() => {

    let socket = null;

    let reconnectTimer =
      null;

    let mounted = true;

    function connect() {

      if (!mounted) return;

      console.log(
        "[WS] Connecting..."
      );

      socket =
        new WebSocket(
          "ws://localhost:8000/ws/pipeline"
        );

      /* ===============================
         CONNECTION OPEN
      =============================== */

      socket.onopen =
        () => {

          console.log(
            "[WS] Connected"
          );
        };

      /* ===============================
         RECEIVE EVENT
      =============================== */

      socket.onmessage =
        (e) => {

          try {

            const event =
              JSON.parse(
                e.data
              );

            dispatch({
              type:
                "PIPELINE_EVENT",

              payload:
                event,
            });

          } catch (err) {

            console.error(
              "[WS] Invalid JSON",
              err
            );
          }
        };

      /* ===============================
         CONNECTION ERROR
      =============================== */

      socket.onerror =
        (err) => {

          console.error(
            "[WS] Error",
            err
          );
        };

      /* ===============================
         CONNECTION CLOSED

         Auto Reconnect
      =============================== */

      socket.onclose =
        () => {

          console.warn(
            "[WS] Disconnected"
          );

          if (!mounted)
            return;

          reconnectTimer =
            setTimeout(
              connect,
              2000
            );
        };
    }

    connect();

    return () => {

      mounted = false;

      clearTimeout(
        reconnectTimer
      );

      socket?.close();
    };

  }, [dispatch]);
}