import React, {Component} from 'react';

export class ResultadoFull extends Component{
    mostrarMedicines = () => {
        const medicines = this.props.medicines;
        const genericos = this.props.genericos;

        if (medicines.length === 0) return  null;

        if (genericos.length === 0) return  null;


        console.log(medicines);
        console.log(genericos)
        return(
            <React.Fragment>
                <h5  >Resultados de Cafam</h5>
                <div className="col-12 p5 row card card-body">
                
                    <table className = "table table-striped col-6 p5 row">
                    <thead >
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

                    <table className = "table table-striped col-6 p5 row">
                    <thead >
                        <tr>
                            <th>Generico </th>
                            <th>Precio </th>
                            
                        </tr>
                    </thead>
                    <tbody>
                    {genericos.map(generico => (
                        <tr key = {generico.medicamento }>
                            <td> {generico.medicamento} </td>
                            <td> {generico.precio} </td>

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
