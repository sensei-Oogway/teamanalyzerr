export default function routes(app, addon) {
    // Redirect root path to /atlassian-connect.json,
    // which will be served by atlassian-connect-express.
    app.get('/', (req, res) => {
        res.redirect('/atlassian-connect.json');
    });

    app.get('/get-collab', addon.authenticate(), (req, res) => {
        var httpClient = addon.httpClient(req);
        
        //Get all projects visible to the user
        httpClient.get('/rest/api/3/project/search', function (err, response, body) {
            var obj = JSON.parse(body);

            var projectKeys = [];
            
            //Iterate through the data and add to the projectKeys
            for(var project of obj.values){
                projectKeys.push(project.key)
            }

            console.log(projectKeys.join(" "))
            
            res.render(
                'collab.hbs',
                {
                    title: 'My little app',
                    projects: projectKeys.join(" ")
                }
            );
        });
    });

    app.get('/get-workload', addon.authenticate(), (req, res) => {
        var projectId = req.query.projectId;
        var httpClient = addon.httpClient(req);

        //Get all boards -> Get all sprints -> Get all users
        httpClient.get('/rest/agile/1.0/board?projectKeyOrId=' + projectId, function (err, response, body) {
            var obj = JSON.parse(body);
            var boardId = obj.values[0].id;

            httpClient.get('/rest/agile/1.0/board/' + boardId + '/sprint', function (err, response, body) {
                //Iterate through sprints
                var obj = JSON.parse(body);
                var retArr = [];

                for (var sprint of obj.values) {
                    var sprint_obj = {};
                    sprint_obj['id'] = sprint.id;
                    sprint_obj['state'] = sprint.state;
                    if (sprint.state == "closed") {
                        sprint_obj['duration'] = ((new Date(sprint.completeDate)) - (new Date(sprint.startDate))) / 1000;

                        //TODO DUMMY value
                        sprint_obj['duration'] = ((new Date(sprint.endDate)) - (new Date(sprint.startDate))) / 1000;
                    } else if (sprint.state == "active") {
                        sprint_obj['duration'] = ((new Date(sprint.endDate)) - (new Date(sprint.startDate))) / 1000;
                    }
                    retArr.push(sprint_obj)
                }

                res.render('workload.hbs', { title: "Workload per project", sprints: JSON.stringify(retArr) });
            });

        });
    });
}
