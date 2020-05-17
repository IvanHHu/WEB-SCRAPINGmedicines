import React, {Component} from 'react'
import {ResultadoBD} from './ResultadoBD'


const API = process.env.REACT_APP_API;
export class SearchBD extends Component {

    state = {
        medicine : '',
        medicines : []
    }

   
    consultarApi = async() => {
        await fetch(`${API}/get_medicine/`+ this.state.medicine)
         .then(respuesta => respuesta.json() )
         //.then(resultado => console.log(resultado) )
         .then(resultado => this.setState( { medicines : resultado}) )

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
            <div>
                <p className="lead text-center"> Busca un medicamento en nuestros datos</p>
                <form onSubmit = {this.obtenerDatos} className="card card-body">
                    <div className="row">
                                <div className=" form-group col-md-9">
                                    <input ref = {this.busquedaRef} type="text" className="form-control"
                                            placeholder= "Busca un medicamento..."/>
                                </div>
                                <div className="form-group col-md-3"  >
                                    <input type="submit" className = "btn btn-lg btn-danger btn-block" value="Buscar"/>
                                </div>  
                    </div>
                    <ResultadoBD
                        medicines = {this.state.medicines}
                    />
                    
                </form>
            </div>
            
        )
    }
        
}
