import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";

import {
PipelineProvider,
} from "./context/PipelineContext";

import "./styles/main.css";

/* ==========================================
APPLICATION ENTRY POINT

Frontend Owner:
Ayushman (P3)

Wraps entire application with
PipelineProvider so all components
can access:

* stages
* verifyResult
* commitment_hex
* verified_zero

via React Context
========================================== */

ReactDOM.createRoot(
document.getElementById("root")
).render(

<React.StrictMode>

```
<PipelineProvider>

  <App />

</PipelineProvider>
```

</React.StrictMode>

);
