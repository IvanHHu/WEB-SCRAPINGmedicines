import React, {Component} from 'react';

export class Resultado extends Component{
    mostrarMedicines = () => {
        const medicines = this.props.medicines;
        if (medicines.length === 0) return  null;

        console.log(medicines);
        return(
            <React.Fragment>
                <div className="col-12 p5 row">
                <table className = "table table-striped">
                <thead >
                    <h2>Resultados de Cafam</h2>
                    <tr>
                        <th>Medicamento </th>
                        <th>Precio </th>
                    </tr>
                </thead>
                <tbody>
                {medicines.map(medicine => (
                    <tr key = {medicine.medicamento }>
                        <td> {medicine.medicamento} </td>
                        <td> {medicine.precio} </td>

                    </tr>
                ))}
                </tbody>
            </table>
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
