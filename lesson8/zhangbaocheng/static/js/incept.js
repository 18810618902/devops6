
$('.sqldetail').click(function(){
  var sqlcontent = $(this).attr('ckvalue')
  $('#infomodal').modal({show:true, backdrop:'static'})
  sqllist = sqlcontent.split(';')
  sqlhtml = ''
  for (i=0;i<sqllist.length;i++){
      if(sqllist[i] == ''){break}  // 不要最后那个多余的分号
      sqlhtml = sqlhtml + '<div>' + sqllist[i] + ';' + '</div>'
  }
  $('#inforz').html(sqlhtml)
  $('#infotitle').html('SQL详情')
})

$('.opsqldetail').click(function(){
  var sqlcontent = $(this).attr('ckvalue')
  $('#infomodal').modal({show:true, backdrop:'static'})
  $('.modal-dialog').css({'width':'80%', 'height':'60%'})
  $('#inforz').html('<pre>' + sqlcontent + '</pre>')
  $('#prompttitle').html('优化建议')
})

$('.sqltailbtn').click(function(){
  var failcontent = $(this).attr('ckvalue')
  $('#infomodal').modal({show:true, backdrop:'static'})
  $('#inforz').html(failcontent)
  $('#infotitle').html('失败详情')
})

$('.sqlnote').click(function(){
  var notecontent = $(this).attr('ckvalue')
  $('#infomodal').modal({show:true, backdrop:'static'})
  $('#inforz').html(notecontent)
  $('#infotitle').html('备注')
})

$(".sqlaction").click(function(){
  var $this =$(this)
  var sqlid = $this.attr('ckid')
  var actiontype = $this.attr('actiontype')

  $('.sqlaction').attr({"disabled":"disabled"})  // 所有按钮禁用
  if (actiontype=='approve'){
	$('#actioncontent').html('审批此SQL？')
	}
  else if (actiontype=='excute'){
	$('#actioncontent').html('执行此SQL到数据库？')
	}
  else if (actiontype=='reject'){
	$('#actioncontent').html('放弃此SQL？')
	}
  else if (actiontype=='pause'){
	$('#actioncontent').html('暂停此SQL？')
	}
  else if (actiontype=='nopause'){
	$('#actioncontent').html('取消暂停此SQL？')
	}
  else if (actiontype=='rollback'){
	$('#actioncontent').html('确定回滚本SQL？')
	}
  $('#action').modal({show:true, backdrop:'static'}) 
  
  $('#actioncancel').click(function(){
	$('#action').modal('hide') 
	$('.sqlaction').removeAttr("disabled")  // 所有按钮启用 
  })
  $("#actionsave").unbind('click').bind('click',function(){  
    $('#action').modal('hide')  
    $this.parent().parent().children().children('#imgloading').show() 
    $.ajax({
             type: "POST",
             url: "/sql/action/",
             data: {sqlid:sqlid, actiontype:actiontype},
             dataType: "json",
             success: function(data){
		$this.parent().parent().children().children('#imgloading').hide() 
		if (actiontype=='excute'){
		    if (data.info=='ok'){
			var Warninghtml = '<p> </p>'
                        if(data.Warning != "") {
                            Warninghtml = '<p>Warning：' + data.Warning + '</p>'
                        }
                        htmlcontent = '<p>' + 'SQL执行结果：' + data.info + '</p>' + '<p>' + '受影响的行：' + data.affected_rows + '</p>' + '<p>' + '时间：' + data.execute_time + '</p>' + Warninghtml
		    }
		    else if (data.info=='statuschange'){
                        htmlcontent = '<p>' + 'SQL状态已被改变' + '</p>'
		    }
		    else {
                        htmlcontent = data.info
		    }
        	}
		else if (actiontype=='rollback'){
		    if (data.info=='ok'){
			htmlcontent = '<p> SQL回滚结果：' + data.info + ' </p>' + '<p> 影响的行数：' + data.rollnum + ' </p>' 
			}
		    else{
			htmlcontent = '<p> SQL回滚失败 </p>'
			}
		}
		else if (actiontype=='pause'){
		    if (data.info=='ok'){
			htmlcontent = '<p> SQL已暂停 </p>'
		    }
		}
		else if (actiontype=='nopause'){
		    if (data.info=='ok'){
			htmlcontent = '<p> SQL已取消暂停 </p>'
		    }
		}
		else if (actiontype=='reject'){
		    if (data.info=='ok'){
			htmlcontent = '<p> SQL已放弃 </p>'
		    }
		}
		else if (actiontype=='approve'){
		    if (data.info=='ok'){
			htmlcontent = '<p> SQL已审批 </p>'
		    }
		}

                $('#infomodal').modal({show:true, backdrop:'static'})
                $('#inforz').html(htmlcontent)

		$('#infoclose').click(function(){
		    var urltag = $('.urltag').attr('ckvalue')
            if(urltag == 'list'){
                location.reload()
		    }
		    else if(urltag == 'detail'){
		        var sqlid = $('.urltag').attr('sqlid')
                location.href = "/sql/sqldetail/?id=" + sqlid
		    }
		})

             },
	     error: function(){
	     },
	})

	})
    })

// 删除优化的sql
 $('.sqldelete').unbind('click').bind('click', function(){
        var deleteid = $(this).attr('ckid')
        var url = "/sql/sqldelete/"
        $('#action').modal({show:true, backdrop:'static'})
        $('#actioncontent').html('<span>确认删除该记录吗？</span>')
        $('#actionsave').unbind('click').bind('click', function(){
                $.ajax({
                        type: "POST",
                        url: url,
                        data: {deleteid:deleteid},
                        dataType: "json",
                        success: function(data){
                            if ( data.status == 0 ){
                                name = data.name
                                $('#action').modal('hide')
                                $('#infomodaldialog').css('text-align', 'center')
                                $('#infomodaldialog').css('width','30%')
                                $('#infomodal').modal({show:true, backdrop:'static'})  // 弹起提示的模态框
                                $('#inforz').html('<span>删除成功！</span>')
                                $('#infoclose').click(function(){
                                        location.reload()
                                    })
                                }
                        },
                        error: function(){
                                console.log('404..')
                        },
                })

        })
 })

