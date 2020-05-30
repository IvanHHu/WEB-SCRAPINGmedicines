import React, {Component} from 'react'
import {ResultadoBD} from './ResultadoBD'
import {ResultadoPre} from './ResultadoPre'


const API = process.env.REACT_APP_API;
export class SearchPre extends Component {

    state = {
        medicine : '',
        medicines : [],
        presentaciones : []
    }

   
    consultarApi = async() => {
        await fetch(`${API}/get_medicine2/`+ this.state.medicine)
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
                                    <input type="submit" className = "btn btn-lg btn-primary btn-block" value="Buscar"/>
                                </div>  
                    </div>
                    <ResultadoPre
                        medicines = {this.state.medicines}
                    />
                    
                </form>
            </div>
            
        )
    }
        
}
