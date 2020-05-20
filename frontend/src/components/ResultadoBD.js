import React, {Component} from 'react';
import {ResultadoFull} from './ResultadoFull'


const API = process.env.REACT_APP_API;

export class ResultadoBD extends Component{

    state = {
        medicine : '',
        generico : '',
        medicines : [],
        genericos : [],
        medicinesCV : [],
        genericosCV : [],
        medicinesLC : [],
        genericosLC : [],
        wiki : []
    }

    consultarApi = async() => {
        //consultas a cafam
        var arreglos = ''
        var arreglos2 = ''
        const res  =  await fetch(`${API}/cafam/`+ this.state.medicine)
        const data = await res.json();
        const arrays = data.length
        const resG  =  await fetch(`${API}/cafam/`+ this.state.generico)
        const dataG = await resG.json();
        const arrays2 = dataG.length

        //consultas a Cruz verde
        var arreglosCV = '';
        var arreglos2CV = '';
        const resCV  =  await fetch(`${API}/cruzverde/`+ this.state.medicine)
        const dataCV = await resCV.json();
        const arraysCV = dataCV.length
        const resGCV  =  await fetch(`${API}/cruzverde/`+ this.state.generico)
        const dataGCV = await resGCV.json();
        const arrays2CV = dataGCV.length

        //consultas a locatel
        var arreglosLC = '';
        var arreglos2LC = '';
        const resLC  =  await fetch(`${API}/locatel/`+ this.state.medicine)
        const dataLC = await resLC.json();
        const arraysLC = dataLC.length
        const resGLC  =  await fetch(`${API}/locatel/`+ this.state.generico)
        const dataGLC = await resGLC.json();
        const arrays2LC = dataGLC.length

        //consulta a wikipedia
        const resWiki  =  await fetch(`${API}/wiki/`+ this.state.generico)
        const dataWiki = await resWiki.json();


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
        if (arrays2 > 1){
            for (var i = 0; i < arrays2 -1; i++) {
                if (arreglos2 === ''){
                    arreglos2 = dataG[i].concat(dataG[i + 1]);
                }
                else{
                    arreglos2 = arreglos2.concat(dataG[i + 1 ])
                }
    
            }
        }
        else{
            arreglos2 = dataG[0]
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
        if (arrays2CV > 1){
            for (var i = 0; i < arrays2CV -1; i++) {
                if (arreglos2CV === ''){
                    arreglos2CV = dataGCV[i].concat(dataGCV[i + 1]);
                }
                else{
                    arreglos2CV = arreglos2CV.concat(dataGCV[i + 1 ])
                }
    
            }
        }
        else{
            arreglos2CV = dataGCV[0]
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
        if (arrays2LC > 1){
            for (var i = 0; i < arrays2LC -1; i++) {
                if (arreglos2LC === ''){
                    arreglos2LC = dataGLC[i].concat(dataGLC[i + 1]);
                }
                else{
                    arreglos2LC = arreglos2LC.concat(dataGLC[i + 1 ])
                }
            }
        }
        else{
            arreglos2LC = dataGLC[0]
        }
        //console.log(arreglos , arreglos2)
        //console.log(arreglosCV , arreglos2CV)
        //console.log(arreglosLC , arreglos2LC)
        //console.log(dataWiki)
        this.setState( {medicines : arreglos, genericos : arreglos2, medicinesCV : arreglosCV, genericosCV : arreglos2CV,medicinesLC : arreglosLC, genericosLC : arreglos2LC, wiki: dataWiki })

    }


    sendMedicamento =(medicine,generico) => {
        this.setState({
            medicine,generico
        }, () => {
            this.consultarApi();
        })
    }

    
    mostrarMedicines = () => {
        const medicines = this.props.medicines;
        if (medicines.length === 0) return  null;

        return(
            <React.Fragment>
                <div className="col-12 p5 row">
                    <ResultadoFull
                        medicines = {this.state.medicines}
                        genericos = {this.state.genericos}
                        medicinesCV = {this.state.medicinesCV}
                        genericosCV = {this.state.genericosCV}
                        medicinesLC = {this.state.medicinesLC}
                        genericosLC = {this.state.genericosLC}
                        wiki = {this.state.wiki}
                        
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