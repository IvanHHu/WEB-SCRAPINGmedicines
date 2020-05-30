import React, {Component} from 'react';
import {ResultadoFull} from './ResultadoFull';
import {ModalPre} from './ModalPre';
import {Button, ButtonToolbar}  from 'react-bootstrap';

const API = process.env.REACT_APP_API;

export class ResultadoPre extends Component{

    state = {
        medicine : '',
        generico : '',
        loading : false,
        showModal: false,
        presentaciones: []
    }

    consultarApi = async() => {
        this.setState({loading: true})
        //consulta a presentaciones
        const res  =  await fetch(`${API}/get_medicine3/`+ this.state.medicine)
        const data = await res.json();
        console.log(data)
        this.setState( {presentaciones : data })
    }


    sendMedicamento =(medicine,generico) => {
        this.setState({
            medicine,generico, showModal: true
        }, () => {
            this.consultarApi();
        })
    }

    
    render(){

        const {loading} = this.state;

        const medicines = this.props.medicines;
        if (medicines.length === 0) return  null;


        let modalClose = () => this.setState({showModal : false})

        return(
            
            <div className="col-12 p5 row">
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
                            <td> {medicine.producto} </td>
                            <td> {medicine.generico} </td>
                            
                            <td>  
                                <ButtonToolbar>
                                    <Button
                                        variant = 'primary'
                                        onClick = {() => this.sendMedicamento( medicine.producto, medicine.generico ) } >
                                        Buscar
                                    </Button>
                                </ButtonToolbar>

                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
                    <ModalPre
                        show = { this.state.showModal}
                        medicine = { this.state.medicine}
                        generico = {this.state.generico}
                        onHide = {modalClose}
                        presentaciones = { this.state.presentaciones }
                    />
            
            </div>

                 
        )
    }

}