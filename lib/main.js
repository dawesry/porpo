import * as ReactDOM from "react-dom/client";
import * as React from "react";
import { StyledEngineProvider } from '@mui/material/styles';
import Alert from './assets/scripts/alert.tsx';
ReactDOM.createRoot(document.querySelector("#alert")).render(<React.StrictMode>
    <StyledEngineProvider injectFirst>
      <Alert />
    </StyledEngineProvider>
  </React.StrictMode>);
