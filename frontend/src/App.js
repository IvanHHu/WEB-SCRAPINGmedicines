import React from 'react';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import {About} from './components/About'
import {Medicines} from './components/Medicines'
import {Navbar} from './components/Navbar'

function App() {
  return (
    <Router>
      <Navbar/>
      <div className="container p-4">
        <Switch>
          <Route path="/about" component={About}  />
          <Route path="/" component={Medicines}  />
        </Switch>
      </div>
    </Router>
  );
}

export default App;
