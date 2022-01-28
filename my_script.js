// 当前的服务状态
var state = {
  // 保存字段的原始值, 用于修改后的复原
  'action': '',
  'settings': '',
  'log': '',
  // api调用返回数据
  'res_data': null
}

function on_action_change() {
  action = get_action_value()
  console.log(action)
  if (action != 'none') {
    url = '/api/settings/get'
    data = {
      'action': action
    }
    request_post(url, data)
  }
}

function on_run_clicked() {
  url = '/api/run'
  data = {
    'action': get_action_value(),
    'settings': get_settings_value(),
    'offset': 0
  }
  disable_run_button(true)
  request_post(url, data)
}

// 请求服务器功能，返回数据用于更新用户界面内容
// url_path: '/api/get?action="list_groups"'
// return json data

function request_logs() {
    url = '/api/logs/get'
    data = state['res_data']
    request_post(url, data)
}

// 请求服务器功能，返回json数据更新界面
//  url - 服务功能的URL
//  data：{
//    action: '..',
//    ...
//  } - 功能及参数（json)
function request_post(url, data) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", url);
  xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

  xhr.onload = function() {
    if (xhr.status == '200') {
      response_data = JSON.parse(xhr.responseText)
    } else {
      response_data = {
        "msg": xhr.statusText
      }
    }
    state['res_data'] = response_data['data']
    update_fields(response_data)

    if (response_data['state'] == 'more') {
      setTimeout(request_logs, 2000)
    }
  }

  xhr.send(JSON.stringify(data));
}

// 用服务器返回的新数据更新用户界面字段内容，数据格式如下：
// "response_date" : {
//   "data": {
//     "action": "text value",
//     "settings": "text value",
//     "offset": 0,  // for log
//     "log": "text value"
//   },
//   ...
// }
function update_fields(response_data) {
  console.log(response_data)
  data = response_data['data']

  if ('action' in data) {
    if (state['action'] != data['action']) {
      state['action'] = data['action']
      set_action_value(state['action'])
    }
  }

  if ('settings' in data) {
    if (state['settings'] != data['settings']) {
      state['settings'] = data['settings']
      set_settings_value(state['settings'])
    }
  }

  if ('log' in data) {
    if (data['offset'] == 0) {
      state['log'] = data['log']
    } else {
      state['log'] += data['log']
    }
    set_log_value(state['log'])
  }

  if (response_data['state'] == 'more') {
    disable_run_button(true)
  } else {
    disable_run_button(false)
  }
}

function get_action_value() {
  return document.getElementById("action").value
}

function get_settings_value() {
  return document.getElementById("settings").value
}

function set_action_value(v) {
  document.getElementById("action").value = v
}

function set_settings_value(v) {
  document.getElementById("settings").value = v
}

function set_log_value(v) {
  document.getElementById("log").value = v
}

function disable_run_button(disable) {
  document.getElementById("run").disabled = disable
}
