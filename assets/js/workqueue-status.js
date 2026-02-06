var global_id = 1;
var cache = {};

const wrapper = d3.select("#wrapper");
const tooltip = d3.select("#wrapper > div.tooltip");
const reload  = d3.select("#reload");


reload.property("checked", localStorage.getItem("reload") == "true");


const API_URL = "https://catalog.cse.nd.edu/query/" + build_filter();
const WINDOW_BASE = window.location.href.split("?")[0];


// query data
d3.json(API_URL, function(data) {
    for (var i=0; i < data.length; i++) {
        add_manager(data[i]);
    }

    // restore scroll position
    if (localStorage.getItem('scrollPosition') !== null) {
        window.scrollTo(0, localStorage.getItem('scrollPosition'));
    }
});


// save scroll position
window.addEventListener('scroll', function() {
    localStorage.setItem('scrollPosition', window.scrollY);
}, false);


d3.select("#title").on("click", function() {
    // clear filters
    window.location = window.location.toString().split("?")[0];
})

// auto-reload
setTimeout(function() {
    if (reload.property("checked")) {
        window.location.reload();
    }
}, 10000);


// on change to auto-reload, reload first
d3.select("#reload").on("change", function() {
    checked = reload.property("checked");
    localStorage.setItem("reload", checked);

    if (checked) {
        window.location.reload();
    }
})


function build_filter() {
    filter = 'type=="wq_master"';

    host = get_query_string_value("host");
    if (host) {
        filter += ' and like(name + ":" + port, "' + host + '")';
    }

    owner = get_query_string_value("owner");
    if (owner) {
        filter += ' and like(owner, "' + owner + '")';
    }

    project = get_query_string_value("project");
    if (project) {
        filter += 'and like(project, "' + project + '")';
    }

    return btoa(filter);
}


function get_query_string_value(key) {
    // https://stackoverflow.com/a/9870540
    return decodeURIComponent(
        window.location.search.replace(
            new RegExp("^(?:.*[&\\?]" + encodeURIComponent(key).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$",
            "i"
            )
        , "$1"
        )
    );
}


function add_manager(manager) {
    var row = wrapper.append("div").attr("class", "row manager").attr("id", manager.name + ":" + manager.port);

    var left = row.append("div").attr("class", "col-md-4");
    var center = row.append("div").attr("class", "col-md-4");
    var right = row.append("div").attr("class", "col-md-4");

    create_table(manager, left);

    if (manager.version[0] >= 7) {
        create_manager_graph(manager, center);
        center.append("hr");
    }

    create_task_status_bar(manager, center);
    create_manager_time_pie(manager, right);

    if (manager.version[0] >= 8) {
        create_worker_tasks_tabs(wrapper, manager);
    }
}

function create_table(manager, column) {
	var table = column.append("div").attr("class", "table-responsive").append("table").attr("class", "table table-sm").append("tbody");

	var host = manager.name + ":" + manager.port;

    var rows = ["Host:", "Project:", "Owner:", "Version:"];
	var data = [host, manager.project, manager.owner, manager.version];
	var keys = ["host", "project", "owner"];

    var catalog_url = "https://catalog.cse.nd.edu/detail/" + manager.address + ":" + manager.port + ":" + manager.name;

	for(i = 0; rows[i]; i++) {
	    var row = table.append("tr");
	    row.append("th").text(rows[i]);

	    var td = row.append("td");

	    // inject link into first row
	    if (i == 0) {
	        td.append("a").attr("href", catalog_url).text(data[i]);
	    } else {
	        td.text(data[i]);
	    }

	    td = row.append("td");

	    // add links to filter result sets
	    if (i != 3) {
	        td.append("a")
	          .attr("href", WINDOW_BASE + "?" + keys[i] + "=" + data[i])
	          .attr("title", "Track " + data[i])
	          .append("i")
	            .attr("class", "fa fa-share");
	    }
	}

}


function create_manager_graph(manager, column) {
    column.append("div").attr("class", "col-md-12").append("label").text("Worker Resources").attr("align","center")
    var innerRight = column.append("div").attr("class", "col-md-12")
    create_graph(manager, innerRight, 300, 120)
}


function create_worker_graph(worker, column) {
    create_graph(worker, column, 300, 120)
}


function create_graph(manager, column, w, h) {
    var data = [
      {
        "group": "Tasks",
        "inuse": manager.tasks_running,
        "total": manager.tasks_waiting,
	"capacity" : manager.capacity_weighted,
      },
      {
        "group": "Workers",
        "inuse": manager.workers_busy,
        "total": manager.workers_connected,
	"capacity" : 0
      },
      {
        "group": "Cores",
        "inuse": manager.cores_inuse,
        "total": manager.cores_total,
	"capacity" : manager.capacity_cores
      },
      {
        "group": "Memory",
        "inuse": manager.memory_inuse / 1024,
        "total": manager.memory_total / 1024,
	"capacity" : manager.capacity_memory,
      },
      {
        "group": "Disk",
        "inuse": manager.disk_inuse / 1024,
        "total": manager.disk_total / 1024,
	"capacity" : manager.capacity_disk
      },
      {
        "group": "GPU",
        "inuse": manager.gpus_inuse,
        "total": manager.gpus_total,
	"capacity" : manager.capacity_gpus
      }
    ];

    var groups = data.map(function(d) { return d.group });  // [Cores, Memory, Disk, GPU]
    var subgroups = ["inuse", "unused", "capacity"];

    data.forEach(function(d) {
        // calculate amount left
        d["unused"] = d["total"] - d["inuse"];
    })

    // set the dimensions and margins of the graph
    var margin = {top: 0, right: 10, bottom: 20, left: 45},
        width = w - margin.left - margin.right,
        height = h - margin.top - margin.bottom;

    // append the svg object to wrapper
    var svg = column
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");
  // Add X axis
  var x = d3.scaleLog()
      .clamp(true)
      .domain([0.1, 1e6])
      .range([0, width]);

  var tickNames = ["0", "1", "10", "100", "1k", "10k", "100k", "1M"];

  svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(
        d3.axisBottom(x)
        .ticks(5)
        .tickFormat(function (d, i) {
            return tickNames[i];
        })
    )

  // Add Y axis
  var y = d3.scaleBand()
    .domain(groups)
    .range([height, 0]);

  svg.append("g")
    .call(
        d3.axisLeft(y).tickSizeOuter(0)
    );

  // color palette = one color per subgroup
  var color = d3.scaleOrdinal()
    .domain(subgroups)
    .range(['#7193b0', '#cad2d9', '#ffffff'])

  // stack the data
  var stackedData = d3.stack()
    .keys(subgroups)
    (data);


  var rect_height = y.bandwidth() * 0.6;

  svg.append("g")
    // bar for each category
    .selectAll("g")
    .data(stackedData)
    .enter().append("g")
      .style("fill", function(d, i) { return color(d.key); })

      // rect for each subgroup (inuse, total)
      .selectAll("rect")
      .data(function(d) { return d; })
      .enter().append("rect")
        .attr("x", function(d) { return x(d[0]); })
        .attr("y", function(d) { return y(d.data.group) + (rect_height / 2) - 3; })
        .attr("height", rect_height)
        .attr("width", function(d) { return x(d[1]) - x(d[0]); })
        .attr("stroke", "grey")
        .on("mouseover", function(d) {
            var group = d.data.group;
            var subgroup = d3.select(this.parentNode).datum().key;
            var subgroupValue = d.data[subgroup];

            if (subgroupValue % 1 != 0) {
                subgroupValue = subgroupValue.toFixed(2);
            }

            var content = parseFloat(subgroupValue).toLocaleString('en-US');
            content += (group == "Memory" || group == "Disk") ? " (GB)" : "";
            content += " " + group + " " + subgroup;

            tooltip
              .text(content)
              .style("opacity", 1)
        })
        .on("mousemove", function(d) {
            mouse = d3.mouse(wrapper.node());
            x = mouse[0] - 30;
            y = mouse[1] - 60;

            tooltip
              .style("opacity", 1)
              .style("left", x + "px")
              .style("top", y + "px")
            })
        .on("mouseleave", function(d) {
            tooltip.style("opacity", 0)
        })
}

function create_task_status_bar(manager, column) {
    column.append("div").attr("class", "col-md-12").append("label").text("Task Progress").attr("align","center")
    var taskContainer = column.append("div").attr("class", "col-md-12");

    var data = [
        manager.tasks_waiting,
        manager.tasks_running,
        manager.tasks_complete - (manager.tasks_failed || 0),
        manager.tasks_failed || 0
    ];

    var categories = [
	"Tasks Waiting",
	"Tasks Running",
	"Tasks Completed",
	"Tasks Failed",
    ];
    var colors = [
	"#cccc55",
	"green",
	"blue",
	"red"
    ];

    var total = data.reduce((a, b) => a + b)

    var cumulativeSum = 0;
    stackedData = []

    data.forEach(function(d, i) {
        var pct = d / total * 100;

        if (pct <= 0) {
            return;
        }

        stackedData.push({
            "x": cumulativeSum,
            "width": pct,
            "category": categories[i],
            "color": colors[i],
            "true_val": d
        })

        cumulativeSum += pct;
    });

    // set the dimensions and margins of the graph
    var width = 250;
    var height = 18;

    // append the svg object to wrapper
    var svg = taskContainer
      .append("svg")
        .attr("width", width)
        .attr("height", height)

    // Add X axis
    var x = d3.scaleLinear()
    .domain([0, 100])
    .range([0, width]);

    svg.append("g")
    .selectAll("rect")
    .data(stackedData)
    .enter().append("rect")
      .attr("x", function(d) { return x(d.x); })
      .attr("y", function(d) { return 0; })
      .attr("height", function(d) { return height; })
      .attr("width", function(d) { return x(d.width); })
      .style("fill", function(d, i) { return d.color; })
      .attr("stroke", "grey")
      .on("mouseover", function(d) {
        var content = d.category + ": " + parseInt(d.true_val).toLocaleString();

        tooltip
          .text(content)
          .style("opacity", 1)
      })
      .on("mousemove", function(d) {
        mouse = d3.mouse(wrapper.node());
        x = mouse[0] - 30;
        y = mouse[1] - 60;

        //x = d3.event.pageX - 40;
        //y = d3.event.pageY - 60;

        tooltip
          .style("opacity", 1)
          .style("left", x + "px")
          .style("top", y + "px")
      })
      .on("mouseleave", function(d) {
        tooltip.style("opacity", 0)
      })
}


function create_manager_time_pie(manager, column) {

    //var innerCol = column.append("div").attr("class", "col inner-col")
    column.append("label").attr("class","col-md-12").text("Manager Time")
    var innerRow = column.append("div").attr("class", "row")
    var pieContainer = innerRow.append("div").attr("class", "col-md-6")
    var pieLegend = innerRow.append("div").attr("class", "col-md-6")

    if(!manager.time_send) return

    var width = 150
    var height = 150
    var margin = 10
    var radius = Math.min(width, height) / 2 - margin

    var svg = pieContainer
	.append("svg")
	.attr("width", width)
	.attr("height",height)
	.append("g")
	.attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    var data = [manager.time_send,manager.time_receive,manager.time_status_msgs,manager.time_internal,manager.time_polling,manager.time_application]
    var labels = ["Send Data", "Recv Data", "Recv Status", "Internal", "Waiting", "Appl Busy"]
    var color = d3.scaleOrdinal(["#ff0000","#0000ff","#ffff00","#00ffff","#00ff00","#aaaaaa"])

    var pie = d3.pie().value(function(d) {return d.value; }).sort(null)
    var data_ready = pie(d3.entries(data))

    var arcGenerator = d3.arc()
	.innerRadius(radius/2)
	.outerRadius(radius)

    svg.selectAll('mySlices')
	.data(data_ready)
	.enter()
	.append('path')
	.attr('d', arcGenerator)
	.attr('fill', function(d){ return(color(d.data.key)) })
	.attr("stroke", "black")
	.style("stroke-width", "1px")
	.style("opacity", 1.0)

    var svg = pieLegend.append("svg").attr("width",width).attr("height",height)
    var size = 15

    svg.selectAll("mydots")
	.data(labels)
	.enter()
	.append("rect")
	.attr("x", size)
	.attr("y", function(d,i){ return size + i*(size+5)}) // 100 is where the first dot appears. 25 is the distance between dots
	.attr("width", size)
	.attr("height", size)
	.style("fill", function(d){ return color(d)})

    svg.selectAll("mylabels")
	.data(labels)
	.enter()
	.append("text")
	.attr("x", size + size*1.2)
	.attr("y", function(d,i){ return size + i*(size+5) + (size/2)}) // 100 is where the first dot appears. 25 is the distance between dots
	.attr("font-size","smaller")
	.text(function(d){ return d})
	.attr("text-anchor", "left")
	.style("alignment-baseline", "middle")
}


function create_worker_tasks_tabs(container, manager) {
    var host = manager.name + ":" + manager.port;

    // create expand link
    var nav = container.append("div")
      .attr("class", "row")
      .style("border-top", "solid 1px #dcdcdc")
      .style("display", "block");

    const target_id = "expandable-" + global_id;

    cache[target_id] = {}

    var ul = nav.append("ul").attr("class", "nav nav-pills nav-fill");

    var wb, tb;

    var worker_status_url = "http://" + host + "/worker_status";
    var task_status_url = "http://" + host + "/task_status";

    // toggle worker button
    wb = ul.append("li").attr("class", "nav-item").append("a")
      .attr("class", "nav-link")
      .text("Worker Details")
      .on("click", function() {
        var target = d3.select("#" + target_id);
        var is_hidden = target.classed("hidden");

        // turn off visibility for all others
        d3.selectAll(".expandable").classed("hidden", true);

        // toggle visibility for current
        var new_is_hidden = !is_hidden && target.attr("state") == "worker";
        target.classed("hidden", new_is_hidden);

        d3.select("a.nav-link.active").classed("active", false);
        wb.classed("active", !new_is_hidden);

        target.attr("state", "worker");

        if (!cache[target_id].hasOwnProperty('worker')) {
            target.html("Loading...");

            d3.json(worker_status_url)
              .timeout(2000)
              .get(function(data) {
                  cache[target_id].worker = data;
                  show_worker_data(target, data, worker_status_url);
              });
        } else {
            show_worker_data(target, cache[target_id].worker, worker_status_url);
        }
      });

    // toggle tasks button
    tb = ul.append("li").attr("class", "nav-item").append("a")
      .attr("class", "nav-link")
      .text("Task Details")
      .on("click", function() {
        var target = d3.select("#" + target_id);
        var is_hidden = target.classed("hidden");

        // turn off visibility for all others
        d3.selectAll(".expandable").classed("hidden", true);

        // toggle visibility for current
        var new_is_hidden = !is_hidden && target.attr("state") == "task";
        target.classed("hidden", new_is_hidden);

        d3.select("a.nav-link.active").classed("active", false);
        tb.classed("active", !new_is_hidden);

        target.attr("state", "task");

        if (!cache[target_id].hasOwnProperty('task')) {
            target.html("Loading...");

            d3.json(task_status_url)
              .timeout(2000)
              .get(function(data) {
                  cache[target_id].task = data;
                  show_task_data(target, cache[target_id].task, task_status_url);
              });
        } else {
            show_task_data(target, cache[target_id].task, task_status_url);
        }
      });

    container.append("div")
      .attr("id", "expandable-" + global_id++)
      .attr("class", "row expandable hidden")
      .attr("state", "");
}


function show_task_data(container, data, refresh_url) {
    if (data == null) {
        container.html("Manager timed out.  No information available.");
        return;
    }

    if (!data || !data.length) {
        container.html("No Task data available.");
        return;
    }

    container.html("");

    var h4 = container.append("h4").text("Tasks");

    // refresh data button
    h4.append("i")
      .attr("class", "fa fa-refresh")
      .on("click", function() {
        container.html("Loading...");

        d3.json(refresh_url)
          .timeout(2000)
          .get(function(data) {
              show_task_data(container, data, refresh_url);

              var id = container.attr("id");
              cache[id].task = data;
          });
      })

    activeTasks = data.filter(task => task.host != null);
    nonActiveTasks = data.filter(task => task.host == null);

    tasks = activeTasks.concat(nonActiveTasks);
    i = 0;
    page_size = 10;

    data = tasks.slice(i, page_size);
    i += page_size;

    var table = container.append("div").attr("class", "table-responsive").append("table").attr("class", "table table-bordered");

    var header = ["host", "command", "disk", "memory", "cores", "gpus"];
    table.append("thead").append("tr").selectAll("th")
     .data(header)
     .enter()
     .append("th")
     .text(function(d) { return d; })

    var tbody = table.append("tbody");

    var tr = tbody.selectAll("tr")
     .data(data)
     .enter()
     .append("tr");

    var td = tr.selectAll("td")
     .data(function(d) { return [d.host, d.command, d.disk, d.memory, d.cores, d.gpus]; })
     .enter()
     .append("td")
     .text(function(d) { return (d == -1) ? "N/A" : d; });

    if (i >= tasks.length) {
        return;
    }

    var div = container.append("div").attr("class", "row");

    div.append("span")
      .text("Load 10 More")
      .attr("class", "more-button")
      .on("click", function(d) {
        var rows = tasks.slice(0, i + page_size);
        i += page_size;

        var tr = tbody.selectAll("tr")
         .data(rows)
         .enter()
         .append("tr");

        //d.state // WAITING, running
        var td = tr.selectAll("td")
         .data(function(d) { return [d.host, d.command, d.disk, d.memory, d.cores, d.gpus]; })
         .enter()
         .append("td")
         .text(function(d) { return (d == -1) ? "N/A" : d; });

        if (i >= tasks.length) {
            d3.selectAll(".more-button").remove();
        }
      });

    div.append("span")
      .text("Load All")
      .attr("class", "more-button")
      .on("click", function(d) {
        var rows = tasks;

        var tr = tbody.selectAll("tr")
         .data(rows)
         .enter()
         .append("tr");

        //d.state // WAITING, running
        var td = tr.selectAll("td")
         .data(function(d) { return [d.host, d.command, d.disk, d.memory, d.cores, d.gpus]; })
         .enter()
         .append("td")
         .text(function(d) { return (d == -1) ? "N/A" : d; });

        d3.selectAll(".more-button").remove();
      });
}


function show_worker_data(container, data, refresh_url) {
    if (data == null) {
        container.html("Manager timed out.  No information available.");
        return;
    }

    if (!data || !data.length) {
        container.html("No Worker data available.");
        return;
    }

    container.html("");

    var h4 = container.append("h4").text("Workers");

    // refresh data button
    h4.append("i")
      .attr("class", "fa fa-refresh")
      .on("click", function() {
        container.html("Loading...");

        d3.json(refresh_url)
          .timeout(2000)
          .get(function(data) {
              show_worker_data(container, data, refresh_url);

              var id = container.attr("id");
              cache[id].worker = data;
          });
      })

    var table = container.append("div").attr("class", "table-responsive").append("table").attr("class", "table table-bordered");

    header = ["host", "command", "resources"];

    table.append("thead").append("tr").selectAll("th")
     .data(header)
     .enter()
     .append("th")
     .text(function(d) { return d; });

    var body = table.append("tbody");

    data.forEach(function(d) {
        var row = body.append("tr");

        row.append("td").text(d.hostname);
        row.append("td").text(d.current_task_000_command);

        var td = row.append("td");
        create_worker_graph(d, td);
    });
}
