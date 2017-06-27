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
    
//

//查看病历详情按钮
    $(".emrbutton").click(function(){
        var patient = $("#patname").text();
        alert(patient);
    });

//项目输入框激活后消除提示信息，获得焦点和离开焦点
    $(".inputitem").focus(function(){
        
            $(this).val('')
    
    });

    $(".inputitem").blur(function(){
        var str =  $(this).val();
        if(str==''){
            $(this).val('输入检查指标')
        }
    });

//统一的按钮点击后，不改变背景颜色
    $(".unibutton").click(function(){
        
        
    });

    //渲染更新网页内容，json
    $(".lista").click(function(){
        var c = $(this).attr('name');
        //alert(c);
        //count = 0;
        $("#"+c).parent().find("table.recognize").each(function(){
           /*复杂了，直接全部不显示后，再令自己显示不就得了
            var show = $(this).css('display');
            if(show=='block'){
                count += 1;
            }
            */
            //$(this).css('display',show =='block'?'none':show);
            $(this).css('display','none');
        });
        $("#"+c).show();

        
    });

    //病历单
    $(".listR").click(function(){
        var c = $(this).attr('name');
        //检查能得到标号数据
        //alert(c),代表此病历单的标识id
        $("#"+c).parent().find("div.onerecord").each(function(){
        //$(".recordspage").find("div.onerecord").each(function(){
            $(this).css('display','none');
        });
        $("#"+c).show();
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
        var idlist = [];//用来记录哪一个或者哪两个被选中，记录它们的id值
        var nolist = [];//用来记录没有被选中的id
        $("#dgtable").find("input").each(function(){ 
            var chooseid = $(this).attr("id")
            var itemtext = $(this).parent().siblings(".dgcontents").text();
            if ($(this).prop("checked")==true) {                 
                chkdis += 1;
                chkall.push(itemtext);
                idlist.push(chooseid);
            }else{
                nolist.push(chooseid);
            }
             
        });

        switch(chkdis)
        {
        case 0:
            alert("您已取消选择，再次点击查看");
            for (var n=0;n<nolist.length;n++){
                var noi = nolist[n]+'dv'
                $("div#"+noi).hide();
            }
            break;
        case 1:
            var id1 = idlist[0]+'dv';
            var noids = ''
            //alert(id1);
            $("div#"+id1).attr("class","col s12 m12 l12");
            //$("div#"+id1).show();
            $("div#"+id1).css('display','');

            for (var n=0;n<nolist.length;n++){
                var noi = nolist[n]+'dv';
                noids += noi
                $("div#"+noi).hide();
            }
            //alert("选中一项")
            //alert(noids)输出没有被选中的id
            break;
        case 2:
            /*
            var id1 = idlist[0];
            var id2 = idlist[1];
            
            alert(id2);
            
            $("div#"+id1).attr("class","mdl-cell mdl-cell--6-col");
            $("div#"+id2).attr("class","mdl-cell mdl-cell--6-col");
            $("div#"+id1).show();
            $("div#"+id2).show();
            */
            //alert("选中两项")
            for (var i=0;i<idlist.length;i++){
                var idi = idlist[i]+'dv';
                $("div#"+idi).attr("class","col s12 m12 l6");
                //$("div#"+idi).show();
                $("div#"+idi).css('display','');
            }

            for (var n=0;n<nolist.length;n++){
                var noi = nolist[n]+'dv';
                //$("div#"+noi).hide();
                $("div#"+noi).css('display','none');
            }
            break;
        default:
            alert("请最多选择两项对比");
            $(this).prop("checked",false)

        }

        
        /*
        //被选中的疾病传回名称和概率等数据，对标签内容进行修改，现在没必要了，现在都是独立的div存放不同的疾病诊断结果和依据
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
        */

    });
    

    //实现获取内部html代码并加到标签元素中内容，要改进实现疾病选中后，界面出现此疾病的详情
    //html方法获取的是内部html代码，不包括本身
    //问题：checkbox的id问题，html代码不能只是简单的复制

    //查看更多诊断结果的按钮，要从数据文件中读取诊断列表，再分别设置到每个tr的内容中去，在添加至网页

    $(".dgbutton").on("click",function(){
        
        $("#dgtable").find("tr.dgtr").each(function(){
            $(this).css('display','');
        });
        /*
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
        */
    });

//添加检查项目
    $(".additem").click(function(e){
        var choiceid = $(this).parent().siblings("div.chooseitems").attr("id");
        //alert(choiceid);
        var ss = choiceid.split('%');
        var chid = ss[0]
        //alert(chid);
        var inputmark = chid+'input'
        var usrinput = $("#"+inputmark).val();
        //alert(usrinput);

        //idvalue是
        var idvalue = $(this).parent().siblings("div.chooseitems").children("span:last-child").children("input").attr("id");
        
        var numss = idvalue.split('%')
        var numstr = numss[1];

        var num = Number(numstr);
        var id = num+1;
        var itemaid = id.toString();
        //numss[0]是疾病的id
        var newidvalue = numss[0]+'%'+itemaid;
        //alert(newidvalue);新添加进来的勾选框的id
        /*如果要把具体的推荐项目的文本值写在外面，id值放到label的属性中，确定提交的方法要改变，添加的方法也要变
        <span style="margin-left: 2px;font-size:12px;"> 
                      <input type="checkbox" class="filled-in" name="selector" id="{{(result['icd_9'])}}*choice%{{i}}" >
                      <label for="{{(result['icd_9'])}}*choice%{{i}}" style="width:300px;" name="{{escape(itemkey)}}">
                        {{escape(items_detail[itemkey])}}</label>
                      </span>
        */
        var anotheritem = "<span style='margin-left: 2px;font-size:12px;'>"+
                      "<input id=" +newidvalue+ " type='checkbox' class='filled-in' name='selector'>"+
                      "<label style='width:300px;' for=" +newidvalue+ ">"+ usrinput +"</label></span>"      
                    
        $(this).parent().siblings("div.chooseitems").append(anotheritem);
        
        //alert(jQuery.type(id));
        

     ////靠获取最后一个input元素中的id值更新id值
     //读取输入框中的检查项目
     /*以前只有一个框的方法
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
        */
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
       //好几个独立的框中的复选框,他们独立的全选操作
       if (formerstate) { 
        $(this).parent().parent().siblings("div.chooseitems").find("input").prop("checked",true);
       }else { // 取消全选 
        $(this).parent().parent().siblings("div.chooseitems").find("input").prop("checked",false);
       }
    　　
        /*以前只有一个框的方法如下括住所示
        //改变子选项
        if (formerstate) { // 全选 
 
        $("#chooseitems").find("input").prop("checked",true)
      }else { // 取消全选 
        $("#chooseitems").find("input").prop("checked",false)
      }
      */
       
    });

//显示更多推荐项目
    $(".recmore").click(function(){
        $(this).parent().parent().siblings("div.chooseitems").find("span").each(function(){
            $(this).css('display','');
        });
    });



//提交所选复选框按钮，获取选中框内检查项目，存入数组中
    $(".admitcheck").click(function(){
        //获取到对应的疾病的id
        var choiceid = $(this).parent().parent().siblings("div.chooseitems").attr("id");
        var ss = choiceid.split('%');
        var diagid = ss[0];
        var patid = $("[name='p_id']").text();
        //创建json文件，并在循环中添加
        //var newchks = new object();——bug
        text = "start";
        
        var chk_value = new Array();

        /*如果要把具体的推荐项目的文本值写在外面，id值放到label的属性中，确定提交的方法要改变，添加的方法也要变
        <span style="margin-left: 5px;font-size:12px;display: none"> 
                      <input type="checkbox" class="filled-in" name="selector" id="{{(result['icd_9'])}}*choice%{{i}}" >
                      <label for="{{(result['icd_9'])}}*choice%{{i}}" style="width:120px;">
                        <a class="tooltipped" data-position="top" data-delay="50" data-tooltip="{{escape(items_detail[itemkey])}}">{{escape(itemkey)}}</a></label>
                      </span>
        */
        //之前一个框时，表达式为$("#chooseitems").find("input")
        $(this).parent().parent().siblings("div.chooseitems").find("input").each(function(){ 
            if ($(this).prop("checked")==true) {  
                
                itemtext = $(this).siblings("label").attr('name');
                text += itemtext;
                chk_value.push(itemtext);
            }  
             
        }); 
        //alert(chk_value)
        //alert(diagid)
        var newobs = {p_id:patid,diseasename:diagid,newdata:chk_value};//key-value object
        var ToStr=JSON.stringify(newobs); 
        //alert(newobs.newdata)
        //数组元素添加到json对象文件中

        //setting
        $.ajaxSetup({
            beforeSend: function(jqXHR, settings) {
                type = settings.type
                if (type != 'GET' && type != 'HEAD' && type != 'OPTIONS') {
                    var pattern = /(.+; *)?_xsrf *= *([^;" ]+)/;
                    var xsrf = pattern.exec(document.cookie);
                    if (xsrf) {
                        jqXHR.setRequestHeader('X-Xsrftoken', xsrf[2]);
                    }
                }
            }});

        $.ajax({
            type: "POST",
            url: "/updiags/testup",//服务器对这个链接进行处理
            data: ToStr,  //传输给服务器的文件必须是json格式
            processData: false,  // tell jQuery not to process the data
            contentType: false,  // tell jQuery not to set contentType
            success: function(data){
                alert("等待后台计算更新数据，若界面自动刷新后暂无变化，请耐心等待并手动再次刷新");
            },
            error: function() {
                //alert("status:"+ XMLHttpRequest.status );
                alert("failure")
                //alert(typeof c);数据类型为str，不是原格式
            }
        });
        
        //点击确定后，将勾选了的检查项目以json格式传到服务器，服务器再操作将其写入数据库
        //document.getElementById(c).style.display=""
        //alert(titem.getAttribute('id'))
        /*
        $.ajax({
            type: "POST",
            url: "/updiags/diagid",//服务器对这个链接进行处理
            data: newchks,  //传输给服务器的文件必须是json格式
            contentType: "application/json;charset=utf-8",
            dataType: "json",//告诉jQuery的返回数据格式
            success: function(data){
                alert("success");
            },
            error: function() {
                //alert("status:"+ XMLHttpRequest.status );
                alert("failure")
                //alert(typeof c);数据类型为str，不是原格式
            }
        });
        */
        //alert(c)
        window.location.reload();//刷新当前界面
    });



  //index界面中病历查看
    $(".subNav").click(function(){

        $(this).toggleClass("currentDd").siblings(".subNav").removeClass("currentDd")

        $(this).toggleClass("currentDt").siblings(".subNav").removeClass("currentDt")

        $(this).next(".navContent").slideToggle(300).siblings(".navContent").slideUp(500)

    });	

    
    

});

