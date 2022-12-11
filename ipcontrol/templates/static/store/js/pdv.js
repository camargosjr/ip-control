function confirmDeletion(event){

    if (confirm("Confirma exclusão da loja?") !==  true){
        event.preventDefault();
    }
        
}

const links = document.querySelectorAll('#ex')

for(let i=0; i< links.length; i++){
    links[i].addEventListener('click', confirmDeletion)
}

