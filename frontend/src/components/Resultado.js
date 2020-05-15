import React, {Component} from 'react';
import Producto from './Producto';

export class Resultado extends Component{
    mostrarMedicines = () => {
        const medicines = this.props.medicines;
        if (medicines.length === 0) return  null;

        console.log(medicines);
        return(
            <React.Fragment>
                <div className="col-12 p5 row">
                <h5>
                Resultados...
                </h5>
                    {medicines.map(medicine => (
                        <Producto
                            key = {medicine.medicamento}
                            medicine =  {medicine}
                        />
                    ))}
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
