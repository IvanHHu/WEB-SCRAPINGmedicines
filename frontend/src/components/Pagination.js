import React from 'react'

export const Pagination =({ medicinesPerPage, totalMedicines, paginate }) => {

    const pageNumbers = [];

    for (let i = 1; i <= Math.ceil(totalMedicines / medicinesPerPage ); i++ ) {
        pageNumbers.push(i);
    }

    return (
        <nav>
            <ul className ="pagination">
                {pageNumbers.map(number => (
                    <li key = {number} className = 'page-item'>
                        <a onClick = {() => paginate(number)}  className = 'page-link'>
                            {number}
                        </a>
                    </li>


                ))}
            </ul>


        </nav>


    )




}
