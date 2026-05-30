/* ==========================================
   API SERVICE

   Frontend Owner:
   Ayushman (P3)

   Backend Owner:
   Animesh (P4)

   Expected Endpoints:

   POST /enrol
   POST /authenticate

   Base URL:
   http://localhost:8000
========================================== */

const API =
  "http://localhost:8000";

/* ==========================================
   ENROLMENT
========================================== */

export async function enrol() {

  try {

    const response =
      await fetch(
        `${API}/enrol`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body:
            JSON.stringify({
              mode: "face",
            }),
        }
      );

    if (!response.ok) {

      throw new Error(
        `Enrol failed: ${response.status}`
      );
    }

    return response;

  } catch (error) {

    console.error(
      "[API] Enrol Error:",
      error
    );

    throw error;
  }
}

/* ==========================================
   AUTHENTICATION
========================================== */

export async function authenticate() {

  try {

    const response =
      await fetch(
        `${API}/authenticate`,
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body:
            JSON.stringify({
              mode: "face",
            }),
        }
      );

    if (!response.ok) {

      throw new Error(
        `Authentication failed: ${response.status}`
      );
    }

    return response;

  } catch (error) {

    console.error(
      "[API] Authentication Error:",
      error
    );

    throw error;
  }
}