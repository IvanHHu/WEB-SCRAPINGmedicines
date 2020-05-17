import React, {Component} from 'react'
import {Resultado} from './Resultado'


const API = process.env.REACT_APP_API;
export class Search extends Component {

    state = {
        medicine : '',
        medicines : []
    }

   
    consultarApi = async() => {
        await fetch(`${API}/cafam/`+ this.state.medicine)
         .then(respuesta => respuesta.json() )
         //.then(resultado => console.log(resultado[0]) )
         .then(resultado => this.setState( { medicines : resultado[0]}) )

    }

    busquedaRef = React.createRef();

    obtenerDatos = (e) => {
        e.preventDefault();
        const medicine = this.busquedaRef.current.value
        this.setState({
            medicine
        }, () => {
            this.consultarApi();
        })
    }
    
    render(){
        return(
            <form onSubmit = {this.obtenerDatos} className="card card-body">
                <div className="row">
                            <div className=" form-group col-md-9">
                                <input ref = {this.busquedaRef} type="text" className="form-control"
                                        placeholder= "Busca en las farmacias..."/>
                            </div>
                                
                            <div className="form-group col-md-3"  >
                                <input type="submit" className = "btn btn-lg btn-danger btn-block" value="Buscar"/>
                            </div>  
                </div>
                <Resultado
                    medicines = {this.state.medicines}
                />
            </form>
            
        )
    }
        
}

//export default Search;