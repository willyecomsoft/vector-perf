function OnUpdate(doc, meta) {
    var repitition = 100

	for (let i = 0; i < repitition; i++) {	  
        meta.id = generateUUID();
        tgt[meta.id]=doc;
    }
}

function generateUUID() {
  // Generate a random number
  var d = new Date().getTime();
  if (typeof performance !== 'undefined' && typeof performance.now === 'function'){
      d += performance.now(); // use high-precision timer if available
  }
  
  // Format the UUID
  var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = (d + Math.random() * 16) % 16 | 0;
    d = Math.floor(d / 16);
    return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
  });

  return uuid;
}