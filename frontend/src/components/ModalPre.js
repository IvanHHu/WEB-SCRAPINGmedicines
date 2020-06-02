import React, {Component} from 'react';
import {Modal, Button, Row, Col, Form } from 'react-bootstrap';
import {ResultadoFull} from './ResultadoFull'

const API = process.env.REACT_APP_API;

export class ModalPre extends Component {

    constructor(props){
        super(props);
    }

    state = {
        medicine : '',
        generico : '',
        presentacion : '',
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

        console.log(this.state.presentacion)
        //consultas a cafam
        const res  =  await fetch(`${API}/cafam/`+ this.state.medicine + this.state.presentacion)
        const data = await res.json();
        const resG  =  await fetch(`${API}/cafam/`+ this.state.generico)
        const dataG = await resG.json();

        //consultas a Cruz verde
        const resCV  =  await fetch(`${API}/cruzverde/`+ this.state.medicine + this.state.presentacion)
        const dataCV = await resCV.json();
        const resGCV  =  await fetch(`${API}/cruzverde/`+ this.state.generico)
        const dataGCV = await resGCV.json();

        //consultas a locatel
        const resLC  =  await fetch(`${API}/locatel/`+ this.state.medicine + this.state.presentacion)
        const dataLC = await resLC.json();
        const resGLC  =  await fetch(`${API}/locatel/`+ this.state.generico)
        const dataGLC = await resGLC.json();
       

        //consulta a wikipedia
        const resWiki  =  await fetch(`${API}/wiki/`+ this.state.generico)
        const dataWiki = await resWiki.json();

        
        
        console.log(data , dataG)
        console.log(dataCV , dataGCV)
        console.log(dataLC , dataGLC)
        console.log(dataWiki)

        setTimeout (() =>{
            this.setState( {medicines : data, genericos : dataG, medicinesCV : dataCV, genericosCV : dataGCV, medicinesLC : dataLC, genericosLC : dataGLC, wiki: dataWiki })
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

    submit = (event) => {
        console.log('Selected value:', event.target.value);
        this.setState({presentacion : event.target.value })
        
      }

    mostrarMedicines = () => {

        const presentaciones = this.props.presentaciones;
        const {loading} = this.state;
        
        if (presentaciones.length === 0) return  null;
        console.log(presentaciones)
        

        return(
            <React.Fragment>
                <Modal
                    {...this.props}
                    size="lg"
                    aria-labelledby="contained-modal-title-vcenter"
                    centered
                    >
                    <Modal.Header closeButton>
                        <Modal.Title id="contained-modal-title-vcenter">
                            Elija una presentacion
                        </Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <div className ="container">
                        <table className = "table table-striped">
                        <thead >
                            <tr>
                                <th><h5>Medicamento</h5></th>
                                <th> <h5> Generico</h5></th>
                                <th> <h5> Presentaciones</h5></th>
                                <th> <h5> Operaciones </h5></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th> {this.props.medicine}   </th>
                                <th> {this.props.generico}   </th>
                            
                        
                                                     
                                <th> <select className="form-control" onChange = {this.submit} >
                                    {presentaciones.map(presentacion => (
                                        <option value = {presentacion.presentacion} >  {presentacion.presentacion} </option> 
                                        ))}
                                    </select>   
                                </th>

                                <th> <button  onClick={() => this.sendMedicamento(this.props.medicine, this.props.generico, this.state.presentacion)} disabled= {loading}
                                    className ="btn btn-lg btn-info btn-block" >
                                    { loading && <i className="fa fa-refresh fa-spin"></i> }
                                    { loading && <span> Buscando en famacias</span> }
                                    { !loading && <span>  Buscar en famacias</span> }
                                    </button>       
                                </th>
     
                        </tr>
                        </tbody>
                        </table>
                        <div>
                            <ResultadoFull
                            medicines = {this.state.medicines}
                            genericos = {this.state.genericos}
                            medicinesCV = {this.state.medicinesCV}
                            genericosCV = {this.state.genericosCV}
                            medicinesLC = {this.state.medicinesLC}
                            genericosLC = {this.state.genericosLC}
                            wiki = {this.state.wiki}
                            
                            />
                        </div>
                            
                        </div>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant= "danger" onClick={this.props.onHide}>Close</Button>
                    </Modal.Footer>

                   

                </Modal>

     
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