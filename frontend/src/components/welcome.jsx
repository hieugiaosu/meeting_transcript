import React from 'react';

const Welcome = ({setWelcome}) => {
    return (
        <div className="welcome m-0 row vh-100">
            <div className="col-md-9">
                <div className="row h-50">
                    <div className="col-md-6">
                        <img
                            src="src/assets/vecteezy_teamwork-or-team-building-office-business-meeting-vector_4154417.svg"
                            className="w-100"
                            alt="Teamwork Illustration"
                        />
                    </div>
                    <div className="col-md-6 gradient-text-welcome d-flex align-items-center">
                        Meet, Talk, Done
                    </div>
                </div>
                <div className="row">
                    <div className="col-md-6 gradient-text-welcome d-flex align-items-center">
                        We Handle the Notes
                    </div>
                    <div className="col-md-6">
                        <img
                            src="src/assets/vecteezy_cartoon-robot-cute-character-pencil-graphic-vector_14919105.svg"
                            className="w-75"
                            alt="Cartoon Robot"
                        />
                    </div>
                </div>
            </div>
            <div className="col-md-3 m-0 p-0 vh-100 welcome-side-bar">
                <div className="fs-2 fw-bold row">Online Transcriber</div>
                <div className="row">
                    <button type="button" className="btn btn-light rounded-pill start-from-welcome" 
                    onClick={ () => {
                        setWelcome(false)
                    }}>
                        Let's start meeting
                    </button>
                </div>
            </div>
        </div>
    );
};

export default Welcome;
