var orign=new Array();//������ǰ����ɫ
var oldTR=null;//�ɵ�tr
var overColor="#88AEFF";//��ͣ��ɫ


function initTable(tblName){
  var obj=document.getElementById(tblName);
  var col=obj.getElementsByTagName("tr");
  for (var i=0;i<col.length;i++){
    col[i].cid=Math.ceil((new Date().getTime())*Math.random());
    orign[col[i].cid]=col[i].style.backgroundColor;
    col[i].onmouseover=function(){this.style.backgroundColor=overColor}
    
    col[i].onmouseout=function(){
      if (oldTR==null||oldTR.cid!=this.cid) this.style.backgroundColor=orign[this.cid];
      
    }
  }
}