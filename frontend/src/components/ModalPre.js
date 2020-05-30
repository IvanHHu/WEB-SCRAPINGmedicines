import React, {Component} from 'react';
import {Modal, Button, Row, Col, Form } from 'react-bootstrap';

const API = process.env.REACT_APP_API;

export class ModalPre extends Component {

    constructor(props){
        super(props);
    }

    state = {
        medicine : '',
        generico : '',
        medicines : [],
        genericos : [],
        loading : false
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

                                <th> <select className="form-control" >
                                    {presentaciones.map(presentacion => (
                                        <option> {presentacion.presentacion} </option> 
                                    ))}

                                    </select>   
                                </th>

                                <th> <button  disabled= {loading}
                                    className ="btn btn-lg btn-info btn-block" >
                                    { loading && <i className="fa fa-refresh fa-spin"></i> }
                                    { loading && <span> Buscando en famacias</span> }
                                    { !loading && <span>  Buscar en famacias</span> }
                                    </button>       </th>
                                
                            </tr>
                        </tbody>
                        </table>
                            
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