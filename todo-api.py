from crypt import methods
import uuid 

from flask import Flask, request, jsonify, abort


# initialize Flask server
app = Flask(__name__)

# create unique id for lists, users, entries
user_id_bob = uuid.uuid4()
user_id_alice = uuid.uuid4()
user_id_eve = uuid.uuid4()

todo_list_1_id = '1318d3d1-d979-47e1-a225-dab1751dbe75'
todo_list_2_id = '3062dc25-6b80-4315-bb1d-a7c86b014c65'
todo_list_3_id = '44b02e00-03bc-451d-8d01-0c67ea866fee'

todo_1_id = uuid.uuid4()
todo_2_id = uuid.uuid4()
todo_3_id = uuid.uuid4()
todo_4_id = uuid.uuid4()

# define internal data structures with example data
user_list = [
    {'id': user_id_bob, 'name': 'Bob'},
    {'id': user_id_alice, 'name': 'Alice'},
    {'id': user_id_eve, 'name': 'Eve'},
]
todo_lists = [
    {'id': todo_list_1_id, 'name': 'Einkaufsliste'},
    {'id': todo_list_2_id, 'name': 'Arbeit'},
    {'id': todo_list_3_id, 'name': 'Privat'},
]
todos = [
    {'id': todo_1_id, 'subject': 'Milch','list': todo_list_1_id, 'owner_id': user_id_bob},
    {'id': todo_2_id, 'subject': 'Arbeitsblätter ausdrucken','list': todo_list_2_id, 'owner_id': user_id_alice},
    {'id': todo_3_id, 'subject': 'Kinokarten kaufen','list': todo_list_3_id, 'owner_id': user_id_eve},
    {'id': todo_3_id, 'subject': 'Eier','list': todo_list_1_id, 'owner_id': user_id_eve},
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

# define endpoint for getting and deleting existing todo lists
@app.route('/list/<list_id>', methods=['GET', 'DELETE'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        print('Returning todo list...')
        return jsonify([i for i in todos if i['list'] == list_id])
    elif request.method == 'DELETE':
        # delete list with given id
        print('Deleting todo list...')
        todo_lists.remove(list_item)
        return '', 200


# define endpoint for adding a new list
@app.route('/list', methods=['POST'])
def add_new_list():
    # make JSON from POST data (even if content type is not set correctly)
    new_list = request.get_json(force=True)
    print('Got new list to be added: {}'.format(new_list))
    # create id for new list, save it and return the list with id
    new_list['id'] = str(uuid.uuid4())
    todo_lists.append(new_list)
    print('Current Lists: {}'.format(todo_lists))
    return jsonify(new_list), 200

#definition endpoint for adding new todo entrys to an distingt list
@app.route('/list/<list_id>/entry',methods = ['POST'])
def add_new_entry(list_id):
    #new entry from POST request
    new_entry = request.get_json(force=True)
    # find todo list depending on given list id
    for l in todo_lists:
        if l['id'] == list_id:
            new_entry['id']=str(uuid.uuid4())
            new_entry['list_id'] = list_id
            todos.append()
            return jsonify(new_entry),200
    abort(400)

@app.route('/list/<list_id>/entry/<entry_id>',methods = ['POST','DELETE'])
def handle_entrys(list_id,entry_id):    
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    # if calling method was post, search for an entry to update
    if request.method == 'POST':
        update_entry=request.get_json(force=True)
        for t in todos:
            if t['id'] == entry_id:
                t = update_entry
                print('Current Todos: {}'.format(todo_lists))
                return '',200
        abort(404)
    elif request.method == 'DELETE':
        for e in todos :
            if e['id'] == entry_id:
                todos.remove(e)
                print('Entry sccesfully removed')
                return '', 200
        abort(404)



# define endpoint for getting all lists
@app.route('/lists', methods=['GET'])
def get_all_lists():
    return jsonify(todo_lists)


if __name__ == '__main__':
    # start Flask server
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
