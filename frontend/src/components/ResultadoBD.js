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
        wiki : [],
        loading : false
    }

    consultarApi = async() => {
        this.setState({loading: true})
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

        arreglos = data
        arreglos2 = dataG
        arreglosCV = dataCV
        arreglos2CV = dataGCV
        arreglosLC = dataLC
        arreglos2LC = dataGLC
        
        console.log(arreglos , arreglos2)
        console.log(arreglosCV , arreglos2CV)
        console.log(arreglosLC , arreglos2LC)
        console.log(dataWiki)

        setTimeout (() =>{
            this.setState( {medicines : arreglos, genericos : arreglos2, medicinesCV : arreglosCV, genericosCV : arreglos2CV,medicinesLC : arreglosLC, genericosLC : arreglos2LC, wiki: dataWiki })
            this.setState({loading : false});

        }, 1000)
        
    }

    sendMedicamento =(medicine,generico) => {
        this.setState({
            medicine,generico
        }, () => {
            this.consultarApi();
        })
    }

    
    mostrarMedicines = () => {
        const {loading} = this.state;

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
                            <td>  <button  onClick={() => this.sendMedicamento(medicine.producto,medicine.generico)} disabled= {loading}
                                    className ="btn btn-lg btn-info btn-block" >
                                    { loading && <i className="fa fa-refresh fa-spin"></i> }
                                    { loading && <span> Buscando en famacias</span> }
                                    { !loading && <span>  Buscar en famacias</span> }
                                    </button>
                                   
                            </td>

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