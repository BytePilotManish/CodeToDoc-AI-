import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import UserProfile from './UserProfile';
import Button from './Button';

function App() {
    return (
        <Router>
            <div className="App">
                <Switch>
                    <Route path="/profile/:id">
                        <UserProfile userId="1" theme="dark" />
                    </Route>
                    <Route path="/">
                        <h1>Home Page</h1>
                        <Button label="Click Me" onClick={() => alert('Hello!')} />
                    </Route>
                </Switch>
            </div>
        </Router>
    );
}

export default App;
