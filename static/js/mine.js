//文档加载完成
$(document).ready(function(){

//测试隐藏功能
    $("p#hidetest").click(function(){
        $(this).hide(1000);
    });

    $("#hide").click(function(){
        $("#hidetest").css("color","blue").slideUp(2000).slideDown(2000);
    });
    $("#show").click(function(){
        $("#hidetest").show(800);
    });
  
    //val() attr() text() html()等方法既能获取也能赋值
    $("#alertbutt").click(function(){
        alert("Value: " + $("#test").val());
    });
    


    //添加检查项目
    $(".additem").click(function(e){
        
     ////靠获取最后一个input元素中的id值更新id值
     //读取输入框中的检查项目
        var usrinput = $("#inputitem").val();
        alert(usrinput);

       var idvalue = $("#chooseitems").children("span:last-child").children("input").attr("id");
       

       var num = Number(idvalue);
       var id = num +1;

        //靠获取点击次数更新id值,标志一共点击的次数
        //arguments.callee.num = arguments.callee.num ? arguments.callee.num : 0;
        // var id = (++arguments.callee.num)+5;

        var itemaid = id.toString();
        var anotheritem = "<span style='margin-left: 5px;'>"+
                      "<input id=" +itemaid+ " type='checkbox' class='filled-in' name='selector'>"+
                      "<label for=" +itemaid+ ">"+ usrinput +"</label></span>"      
                    
        $("#chooseitems").append(anotheritem);
    });

    
  
    //全选检查项目
    $(".chooseall").click(function(){

       /* $("#chooseitems").find("input")(function(){
            if(this.attr("checked")==false){
                this.attr("checked",true)
            }else{
                attr("checked",false)
            }
        });*/
        //点击前的状态
       var formerstate=$(this).prop("checked");
        /*if($(this).prop("checked")){
            formerstate=true;
        }else{
            formerstate=false;
        }*/
        
        //改变子选项
        if (formerstate) { // 全选 
 
        $("#chooseitems").find("input").prop("checked",true)
      }else { // 取消全选 
        $("#chooseitems").find("input").prop("checked",false)
      }
       
    });


//提交按钮，获取选中框内检查项目，存入数组中
    $("#admitcheck").click(function(){
        
        text = "start";
        var chk_value = new Array();
        var box = $("#chooseitems").find("input").each(function(){ 
            if ($(this).prop("checked")==true) {  
                
                itemtext = $(this).siblings("label").text();
                text += itemtext;
                chk_value.push(itemtext);
            }  
             
        }); 

        alert(chk_value.toString());

    });


  //index界面中病历查看
    $(".subNav").click(function(){

        $(this).toggleClass("currentDd").siblings(".subNav").removeClass("currentDd")

        $(this).toggleClass("currentDt").siblings(".subNav").removeClass("currentDt")

        $(this).next(".navContent").slideToggle(300).siblings(".navContent").slideUp(500)

    });	

    
    

});

