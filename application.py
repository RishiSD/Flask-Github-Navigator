from flask import  Flask, request, render_template
from gitnavi import GitNavi

app = Flask(__name__)


@app.route('/navigator')
def navigator():
    """
    The function is bound to the URL and will be invoked once the URL is accessed,
    it renders the output for the search_term on HTML page.
    """
    search_term = request.args.get('search_term')
    git_nav = GitNavi(5)
    render_list = git_nav.search_git_repos(search_term)
    return render_template('template.html', title= 'Github Navigator', search_term=search_term, render_list= render_list )

if __name__ == "__main__":
    """
    The main function to run the Flask App.
    """
    app.debug=True
    app.run()