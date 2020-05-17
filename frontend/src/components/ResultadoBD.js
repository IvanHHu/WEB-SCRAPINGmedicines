import React, {Component} from 'react';
import {ResultadoFull} from './ResultadoFull'


const API = process.env.REACT_APP_API;

export class ResultadoBD extends Component{


    state = {
        medicine : '',
        generico : '',
        medicines : [],
        genericos : []
    }

    consultarApi = async() => {
        var numbers = ''
        var numbers2 = ''
        const res  =  await fetch(`${API}/cafam/`+ this.state.medicine)
        const data = await res.json();
        const arrays = data.length
        
        const resG  =  await fetch(`${API}/cafam/`+ this.state.generico)
        const dataG = await resG.json();
        const arrays2 = dataG.length

        if (arrays > 1){
            for (var i = 0; i < arrays -1; i++) {
                if (numbers === ''){
                    numbers = data[i].concat(data[i + 1]);
                }
                else{
                    numbers = numbers.concat(data[i + 1 ])
                }
    
            }
            console.log(numbers)
           
        }

        if (arrays2 > 1){
            for (var i = 0; i < arrays2 -1; i++) {
                if (numbers2 === ''){
                    numbers2 = dataG[i].concat(dataG[i + 1]);
                }
                else{
                    numbers2 = numbers2.concat(dataG[i + 1 ])
                }
    
            }
            console.log(numbers2)
           
        }

        console.log(arrays)
        console.log(data)
        console.log(arrays2)
        console.log(dataG)
        
        //this.setState( {medicines : numbers, genericos : dataG[0]})

         //.then(respuesta => respuesta.json() )
         //.then(resultado => console.log(resultado[0]) )
         //.then(resultado => this.setState( { medicines : resultado}) )

    }


    sendMedicamento =(medicine,generico) => {
        this.setState({
            medicine,generico
        }, () => {
            this.consultarApi();
        })
        //console.log(medicamento)
    }

    
    mostrarMedicines = () => {
        const medicines = this.props.medicines;
        if (medicines.length === 0) return  null;

        //console.log(medicines);

        return(
            <React.Fragment>
                <div className="col-12 p5 row">
                    <ResultadoFull
                        medicines = {this.state.medicines}
                        genericos = {this.state.genericos}
                    />
                    <table className = "table table-striped">
                    <thead >
                        <tr>
                            <th><h5>Medicamento</h5></th>
                            <th> <h5> Generico</h5></th>
                            <th> <h5> Operaciones </h5></th>
                        </tr>
                    </thead>
                    <tbody>
                    {medicines.map(medicine => (
                        <tr key = {medicine.id}>
                            <td > {medicine.producto} </td>
                            <td> {medicine.generico} </td>
                            <td>  <input type="submit"  onClick={() => this.sendMedicamento(medicine.producto,medicine.generico)} className ="btn btn-lg btn-info btn-block" value="Buscar en farmacias"/> </td>

                        </tr>
                    ))}
                    </tbody>
                    </table>
                    <br></br>
                    
                </div>
            </React.Fragment>
        )
    }
   



    render(){
        return(
            <React.Fragment>
                { this.mostrarMedicines() }
            </React.Fragment>
                 
        )
    }

}