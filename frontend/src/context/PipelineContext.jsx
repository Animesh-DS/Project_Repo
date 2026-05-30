import {
  createContext,
  useReducer,
} from "react";

/* ==========================================
   GLOBAL PIPELINE STATE

   P3 Frontend Owner:
   Ayushman

   Receives events from:
   ws://localhost:8000/ws/pipeline

   Event Format:

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

export const PipelineContext =
  createContext();

/* ==========================================
   INITIAL STATE

   Must match project specification
========================================== */

const initialState = {

  stages: {},

  verifyResult: null,

  commitment_hex: "",

  verified_zero: false,
};

/* ==========================================
   VALID STAGES

   Unknown stages ignored safely
========================================== */

const VALID_STAGES = [
  "capture",
  "preprocess",
  "error_correct",
  "hash",
  "wipe",
  "verify",
];

/* ==========================================
   REDUCER
========================================== */

function reducer(
  state,
  action
) {

  switch (
    action.type
  ) {

    case "PIPELINE_EVENT": {

      const event =
        action.payload;

      const data =
        event.data || {};

      /* ===============================
         Ignore unknown stages
      =============================== */

      const updatedStages =
        VALID_STAGES.includes(
          event.stage
        )
          ? {
              ...state.stages,

              [event.stage]:
                event.status,
            }
          : state.stages;

      let verifyResult =
        state.verifyResult;

      let commitment_hex =
        state.commitment_hex;

      let verified_zero =
        state.verified_zero;

      /* ===============================
         HASH COMPLETE
      =============================== */

      if (
        event.stage === "hash" &&
        event.status === "done"
      ) {

        commitment_hex =
          data.commitment_hex
            ?.slice(0, 8) || "";
      }

      /* ===============================
         MEMORY WIPE VERIFIED
      =============================== */

      if (
        event.stage === "wipe" &&
        event.status === "done"
      ) {

        verified_zero =
          data.verified_zero ??
          false;
      }

      /* ===============================
         NODE VERIFICATION COMPLETE
      =============================== */

      if (
        event.stage === "verify" &&
        event.status === "done"
      ) {

        verifyResult = {

          verified:
            data.verified ??
            false,

          node_votes:
            data.node_votes ||
            [
              false,
              false,
              false,
            ],
        };
      }

      return {

        stages:
          updatedStages,

        verifyResult,

        commitment_hex,

        verified_zero,
      };
    }

    /* ===============================
       RESET PIPELINE
    =============================== */

    case "RESET":

      return initialState;

    default:

      return state;
  }
}

/* ==========================================
   PROVIDER
========================================== */

export function PipelineProvider({
  children,
}) {

  const [
    state,
    dispatch,
  ] = useReducer(
    reducer,
    initialState
  );

  return (

    <PipelineContext.Provider
      value={{
        state,
        dispatch,
      }}
    >

      {children}

    </PipelineContext.Provider>
  );
}