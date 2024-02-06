import React , {Component} from 'react';
import LoginPage from "./LoginPage";
import RegisterPage from "./RegisterPage";
import CodeVerificationPage from "./CodeVerificationPage";
import { BrowserRouter as Router, Routes, Route, Link, Redirect } from 'react-router-dom';

export default class LandingPage extends Component {
    constructor(props){
        super(props);
    }

    render() {
        return <p>This is Landinggg Page</p>
    }
}


