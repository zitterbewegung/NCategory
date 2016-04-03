import 'aframe-core'
import 'babel-polyfill'
import {Animation, Entity, Scene} from 'aframe-react'
import React from 'react'
import ReactDOM from 'react-dom'
import sample from 'lodash.sample'
import {cdn} from '../utils'
import {Camera, Cursor, Light, Sky, CurvedImage, VideoSphere} from '../components/primitives'
import {Sphere, Cube, Cylinder, Plane} from '../components/geometries'
import {
    SearchkitManager,
    SearchkitProvider,
    SearchBox,
    Hits}from "searchkit";
require("./index.scss");
var ReactTHREE = require('react-three');
var THREE = require('three');
var Modal = require('react-modal');

const devhost = "http://192.168.99.100:9200/main_index"
const host = "https://d78cfb11f565e845000.qb0x.com/movies"
const sk = new SearchkitManager(devhost, {
  multipleSearchers:false
})

class ModelHits extends Hits {
    renderResult(result) {
	let url = "https://s3.amazonaws.com/ncategorizer-assets/3d-models/" + result._location
	return (
	        <div className={this.bemBlocks.item().mix(this.bemBlocks.container("item"))} key={result._id}>
		<a href={url} target="_blank">
		
	        <img className={this.bemBlocks.item("thumbnail")} src={result._source.image_file} width="180" height="270"/>
		<div className={this.bemBlocks.item("title")}>{result._source.title}</div>
		<div className={this.bemBlocks.item("description")}>{result._source.description}</div>
		<div className={this.bemBlocks.item("meta_data")}>{result._source.meta_data}</div>
		<div className={this.bemBlocks.item("price")}>{result._source.price}</div>
		<ModalViewer></ModalViewer>		

		</a>
		</div>
	)
    }
}
var ModelRenderer = React.createClass({
    render: function() {
	var aspectratio = this.props.width / this.props.height;
	var cameraprops = {fov : 75, aspect : aspectratio,
			   near : 1, far : 5000,
			   position : new THREE.Vector3(0,0,600),
			   lookat : new THREE.Vector3(0,0,0)};

	return <Renderer width={this.props.width} height={this.props.height}>
	    <Scene width={this.props.width} height={this.props.height} camera="maincamera">
	    <PerspectiveCamera name="maincamera" {...cameraprops} />
	    <Cupcake {...this.props.cupcakedata} />
	    </Scene>
	    </Renderer>;
    }
});
var ModalViewer = React.createClass({

    getInitialState: function() {
	return { modalIsOpen: false };
    },

    openModal: function() {
	this.setState({modalIsOpen: true});
    },

    closeModal: function() {
	this.setState({modalIsOpen: false});
    },

    handleModalCloseRequest: function() {
	// opportunity to validate something and keep the modal open even if it
	// requested to be closed
	this.setState({modalIsOpen: false});
    },

    handleSaveClicked: function(e) {
	alert('Save button was clicked');
    },

    render: function() {
	return (
	    <div class="ModalViewer">
		    <button onClick={this.openModal}>Open Modal</button>
	             <Modal
	    className="Modal__Bootstrap modal-dialog"
	    closeTimeoutMS={150}
	    isOpen={this.state.modalIsOpen}
	    onRequestClose={this.handleModalCloseRequest}
	        >
		<div className="modal-content">
		<div className="modal-header">
		
		<button type="button" className="close" onClick={this.handleModalCloseRequest}>
		<span aria-hidden="true">&times;</span>
		<span className="sr-only">Close</span>
		</button>
		<h4 className="modal-title">Modal title</h4>
		</div>
		<div className="modal-body">
                <ModelRenderer></ModelRenderer>
	        </div>
	        </div>
	        </Modal>
	    </div>
	);
    }
});

class MovieHits extends Hits {
	renderResult(result) {
		let url = "http://www.imdb.com/title/" + result._source.imdbId
	         return (
		
			<div className={this.bemBlocks.item().mix(this.bemBlocks.container("item"))} key={result._id}>
				<a href={url} target="_blank">
					<img className={this.bemBlocks.item("poster")} src={result._source.poster} width="180" height="270"/>
					<div className={this.bemBlocks.item("title")}>{result._source.title}</div>
			        </a>
	                    <ModalViewer></ModalViewer>		
   		        </div>
		)
	}
}
class DemoScene extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}
  }

  render () {

      return (
	  <div>
	      <div className="search-site">
			<SearchkitProvider searchkit={sk}>
				<div>
					<div className="search-site__query">
						<SearchBox autofocus={true} searchOnChange={true}/>
					</div>

					<div className="search-site__results">
						<ModelHits hitsPerPage={10}/>
					</div>
				</div>
			</SearchkitProvider>
	      </div>
       </div>
    )
  }
}


ReactDOM.render(<DemoScene/>, document.querySelector('.scene-container'))

