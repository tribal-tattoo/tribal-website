import firebase from './firebaseInit'
const checkNumber = function(chkArray){
    const isNumber = function(n){
        n = n+''
        n = n.trim();
        const digits_only = string => [...string].every(c => '.0123456789:'.includes(c));
        if(n==""){
          return false;
        }
        if(n.indexOf(' ') > 0){
          return false;
        }
        if(!digits_only(n)){
          return false;
        }
        return true;
    }
    let flag=0;
    chkArray.forEach(element => {

      if(element==undefined || element == null){
        element ="";
      }
      if(!isNumber(element))
      {
        flag=1;
      }
    });
    if(flag==0)
      return true;
    else
      return false;
}
const checkNumberOrEmpty = function(chkArray){
  const isNumber = function(n){
      n = n+''
      n = n.trim();
      const digits_only = string => [...string].every(c => '.0123456789:'.includes(c));
      if(n==""){
        return true;
      }
      if(n.indexOf(' ') > 0){
        return false;
      }
      if(!digits_only(n)){
        return false;
      }
      return true;
  }
  let flag=0;
  chkArray.forEach(element => {

    if(element==undefined || element == null){
      element ="";
    }
    if(!isNumber(element))
    {
      flag=1;
    }
  });
  if(flag==0)
    return true;
  else
    return false;
}
const getDocument = function(reference,$,objectName){
    firebase.db.doc(reference).onSnapshot(snapshot=>{
      $[objectName] = snapshot.data();
    })
    // firebase.db.doc(reference+"/"+$.id).get().then(snapshot => {
    //   $[objectName] = snapshot.data();
    //   console.log($[objectName])
    // }).catch(err=>{
    //   console.log(err);
    // });
}
const getAllDocs = function(reference , $) {
  
  firebase.db.collection(reference).onSnapshot(snapshot => {
    $.documents = [];
      snapshot.forEach(function(doc) {
          $.documents.push(doc.id);
      });
  })
}
const getMonthNumber = function() {
  var d = new Date();
  var n = d.getMonth();
  return n+1;
}
export default {
    checkNumber,
    getDocument,
    getAllDocs,
    getMonthNumber,
    checkNumberOrEmpty,
}