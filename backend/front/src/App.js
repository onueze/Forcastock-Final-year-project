import "./App.css";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Landing from "./components/Landing";
import Register from "./components/Register";
import Login from "./components/Login";
import Navbar from "./components/NavBar";

function App() {
  const myWidth = 220;
  return (
    <div className="App">
        <Navbar
          drawerWidth={myWidth}
          content={
            <Routes>
              <Route path="" element={<Landing />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
            </Routes>
          }
        />
    </div>
  );
}

export default App;
