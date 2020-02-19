function wfAddModal(){
   var wfModal = document.getElementById("workFlow")
   var close = document.getElementsByClassName('popupCloseButton')[0]
   wfModal.style.display = "block"
   close.onclick = function(){
        wfModal.style.display = "none"
   }

}

function wfRetModal(){
   var retModal = document.getElementById("retWorkFlow")
   var closeRet = document.getElementsByClassName('popupCloseButton')[0]
   var close = document.getElementById('close')
   retModal.style.display = "block"
   close.onclick = function(){
        retModal.style.display = "none"
   }
}
