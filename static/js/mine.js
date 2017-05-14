//文档加载完成
$(document).ready(function(){

//测试隐藏功能
    $("#secondpage").hide();
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
    


//查看病历详情按钮
    $(".emrbutton").click(function(){
        var patient = $("#patname").text();
        alert(patient);
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


//勾选对比诊断列表,遇到的问题：动态添加后的元素不能响应事件。解决：要使用到父辈元素绑定事件才能实现。
//获取到tr同胞元素中 被选中的疾病的数量，如果其同胞都没有选中，则此疾病的布局占全屏，如果只有一个同胞被选中，则布局占一半
//多于1个的同胞，则alert出提示信息
    $("#dgtable").on("click", ".onedisease", function(){
        //alert("hello");
        var flag = $(this).prop("checked");
        var disease = $(this).parent().siblings(".dgcontents").text();
        var rate = $(this).parent().siblings(".dgrate").text();
        var chkdis = 0;//点击过后，一共有几个被选中
        var chkall = [];
        $("#dgtable").find("input").each(function(){ 
            if ($(this).prop("checked")==true) {  
                
                var itemtext = $(this).parent().siblings(".dgcontents").text();
                chkdis += 1;
                chkall.push(itemtext);
            }  
             
        });

        switch(chkdis)
        {
        case 0:
            alert("没有选择");
            break;
        case 1:
            alert("hello");
            $($("#mostpage").children("div").get(0)).attr("class","mdl-cell mdl-cell--12-col");
            $($("#mostpage").children("div").get(1)).hide();
            break;
        case 2:
            alert("hello again");
            $($("#mostpage").children("div").get(0)).attr("class","mdl-cell mdl-cell--6-col");
            $($("#mostpage").children("div").get(1)).attr("class","mdl-cell mdl-cell--6-col");
             $($("#mostpage").children("div").get(1)).show();
            break;
        default:
            alert("请最多选择两项对比");
        }

        
        
        //被选中的疾病传回名称和概率等数据，对标签内容进行修改
        if (flag){            
            
            //$(this).parent().siblings(".dgcontents").text("此病被选中");
            
            $(".thedisease").text(disease);
            $(".showrate").text(rate);
        }else{
            //alert(rate);
            //$(this).parent().siblings(".dgcontents").text("此病已恢复");
            $(".thedisease").text("选中疾病");
            $(".showrate").text("概率");
        }
        

    });
    

    //实现获取内部html代码并加到标签元素中内容，要改进实现疾病选中后，界面出现此疾病的详情
    //html方法获取的是内部html代码，不包括本身
    //问题：checkbox的id问题，html代码不能只是简单的复制

    //查看更多结果的按钮，要从数据文件中读取诊断列表，再分别设置到每个tr的内容中去，在添加至网页
    $(".dgbutton").on("click",function(){
        var diseaselist  = ['肝脏','心脏','大脑'];
        var ratelist  = ['33%','44%','55%'];
        var n = 5;
        for (var i=0;i<diseaselist.length;i++){
            var anothertr = "<tr class='dgtr'><td class='dgcontents'>"+diseaselist[i]+"</td><td class='dgrate'>"
                +ratelist[i]+"</td><td class='dgcheck'>"+
                "<input type='checkbox' class='filled-in onedisease' name='selector' id='dgid["+(i+n)+
                "]'><label for='dgid["+(i+n)+"]'></label></td></tr>" ;
            $("#dgtable").append(anothertr);
        }
            
            //var boxhtml = $("#dgtable").html();
            //$("#changebg").toggle();;
            //$("#dgtable").append(boxhtml);
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
        //点击前的状态,自己的js方法比自带的慢，已经变成真的了
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
        $("#chooseitems").find("input").each(function(){ 
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

