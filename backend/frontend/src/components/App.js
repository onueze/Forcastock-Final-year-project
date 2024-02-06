import React, {Component } from "react";
import {render} from "react-dom"
import HomePage from "./HomePage"
import LoginPage from "./LoginPage";
import RegisterPage from "./RegisterPage";
import CodeVerificationPage from "./CodeVerificationPage";
import { Divider } from "@material-ui/core";
import LandingPage from "./LandingPage";
import { BrowserRouter as Router, Routes, Route, Link, Redirect } from 'react-router-dom';


export default class App extends Component {
    constructor(props){
        super(props);
    }
    render(){
        return (
            <Router>
                <Routes>
                    <Route exact path='/' ><p>This is home</p></Route>
                    <Route path='/login' element={<LoginPage/>}></Route>
                    <Route path='/register' element={<RegisterPage/>}></Route>
                </Routes>
            </Router>
        );
        
    }
    
}

const appDiv = document.getElementById("app");
render(<App />,appDiv)
