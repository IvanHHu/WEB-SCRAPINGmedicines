import React, {Component} from 'react';
import {BrowserRouter as Router, Switch, Route} from 'react-router-dom'
import {About} from './components/About'
import {Medicines} from './components/Medicines'
import {Navbar} from './components/Navbar'
import{Search} from './components/Search'
import { Catalogo } from './components/Catalogo'
import { ResultdoFull } from './components/ResultadoFull'

class App extends Component {

render(){
  return (
    <Router>
      <Navbar/>
      <div className="container p-4">
        <Switch>
          <Route path="/about" component={About}  />
          <Route path="/catalogo" component={Catalogo}  />
          <Route path="/search" component={Search}  />
          <Route path="/" component={Medicines}  />
          
        </Switch>
      </div>
      
    </Router>
  );

}

    
}

export default App;
