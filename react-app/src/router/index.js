'use strict'

import React from 'react';
import {HashRouter, Route, Switch} from 'react-router-dom';
import Login from '../views/login/login';
import UserList from '../views/user/list/';

const BasicRoute = () => (
    <HashRouter>
      <Switch>
        <Route exact path="/login" component={Login}/>
        <Route exact path="/user/list" component={UserList}/>
      </Switch>
    </HashRouter>
);


export default BasicRoute;