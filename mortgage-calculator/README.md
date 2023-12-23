# Projects Showcase

## React Mortgage Calculator Tutorial for Beginners

![Thumbnail](path/to/thumbnail/image.png)

### Table of Contents

1. Setup
2. Material UI Theme
3. Navbar
4. MUI Grid System
5. Slider Component


## Setup

To set up the project, follow these steps:

1. Create a folder named `mortgage-calculator`.
2. Open the terminal and run the following commands:
   ```bash
   npx create-react-app .
   npm install @mui/material @emotion/react @emotion/styled
   npm install --save chart.js react-chartjs-2

  ### Material UI Theme
We are using the dark theme of Material UI. Create a file named theme.js in the src folder and add the following code:
```
import {createTheme } from "@mui/material/styles";

export const theme = createTheme({
  palette: {
    mode: "dark",
  },
});

In the index.js file, import the theme and wrap the app with the ThemeProvider.
// index.js
```
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { theme } from "./theme";

<React.StrictMode>
  <ThemeProvider theme={theme}>
    <App />
    <CssBaseline />
  </ThemeProvider>
</React.StrictMode>


   ### Navbar
Next, we will be creating a very simple Navbar to show the Logo. For that, create a file named Navbar.js in the src/Components folder and add the following code:

```
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { Container } from "@mui/system";

const Navbar = () => {
  return (
    <AppBar position="static">
      <Container maxWidth='xl'>
        <Toolbar>
          <Typography variant="h5">
            Bank of React
          </Typography>
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Navbar;

### MUI Grid System
The MUI Grid System allows for a flexible and responsive layout. Create a file named GridSystem.js in the src/Components folder and add the following code:
```
import React from "react";
import { Grid } from "@mui/material";

const GridSystem = () => {
  return (
    {/* Add your grid items here */}
  );
};

export default GridSystem;



### Slider Component
Next, we will create a slider component to get input from the user. It will look like this:

For that, create a file named SliderComponent.js in the src/Components/Common folder. Define the necessary props for the reusable slider component:

```
import React from "react";
import Slider from "@mui/material/Slider";
import { Typography } from "@mui/material";
import { Stack } from "@mui/system";

const SliderComponent = ({
  defaultValue,
  min,
  max,
  label,
  unit,
  onChange,
  amount,
  value,
  steps
}) => {
  return (
    <Stack my={1.4}>
      <Stack gap={1}>
        <Typography variant="subtitle2">{label}</Typography>
        <Typography variant="h5">
          {unit} {amount}
        </Typography>
      </Stack>
      <Slider
        min={min}
        max={max}
        defaultValue={defaultValue}
        aria-label="Default"
        valueLabelDisplay="auto"
        onChange={onChange}
        value={value}
        marks
        step={steps}
      />
      <Stack direction="row" justifyContent="space-between">
        <Typography variant="caption" color="text.secondary">
          {unit} {min}
        </Typography>
        <Typography variant="caption" color="text.secondary">
          {unit} {max}
        </Typography>
      </Stack>
    </Stack>
  );
}

export default SliderComponent;



