import React, {Component} from 'react'
import {Resultado} from './Resultado'


const API = process.env.REACT_APP_API;
export class Search extends Component {

    state = {
        medicine : '',
        medicines : [],
        medicinesCV : [],
        medicinesLC : []

    }

   
    consultarApi = async() => {
            //consultas a cafam
            var arreglos = ''
            const res  =  await fetch(`${API}/cafam/`+ this.state.medicine)
            const data = await res.json();
            const arrays = data.length
    
            //consultas a Cruz verde
            var arreglosCV = '';
            const resCV  =  await fetch(`${API}/cruzverde/`+ this.state.medicine)
            const dataCV = await resCV.json();
            const arraysCV = dataCV.length
    
            //consultas a locatel
            var arreglosLC = '';
            const resLC  =  await fetch(`${API}/locatel/`+ this.state.medicine)
            const dataLC = await resLC.json();
            const arraysLC = dataLC.length
    
            if (arrays > 1){
                for (var i = 0; i < arrays -1; i++) {
                    if (arreglos === ''){
                        arreglos = data[i].concat(data[i + 1]);
                    }
                    else{
                        arreglos = arreglos.concat(data[i + 1 ])
                    }
                }
            }
            else{
                arreglos = data[0]
            }
            
            ///////////////////////////////////////////////////////////////////////////////////////
            
    
            if (arraysCV > 1){
                for (var i = 0; i < arraysCV -1; i++) {
                    if (arreglosCV === ''){
                        arreglosCV = dataCV[i].concat(dataCV[i + 1]);
                    }
                    else{
                        arreglosCV = arreglosCV.concat(dataCV[i + 1 ])
                    }
                }
            }
            else{
                arreglosCV = dataCV[0]
            }
           
    
             ///////////////////////////////////////////////////////////////////////////////////////
            
            if (arraysLC > 1){
                for (var i = 0; i < arraysLC -1; i++) {
                    if (arreglosLC === ''){
                        arreglosLC = dataLC[i].concat(dataLC[i + 1]);
                    }
                    else{
                        arreglosLC = arreglosLC.concat(dataLC[i + 1 ])
                    }
                }
            }
            else{
                arreglosLC = dataLC[0]
            }
            
            //console.log(arreglos)
            //console.log(arreglosCV)
            //console.log(arreglosLC)
            this.setState( {medicines : arreglos, medicinesCV : arreglosCV, medicinesLC : arreglosLC })
    

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
    
    render() {
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
                    medicinesCV = {this.state.medicinesCV}
                    medicinesLC = {this.state.medicinesLC}
                />
            </form>
            
        )
    }
        
}

//export default Search;