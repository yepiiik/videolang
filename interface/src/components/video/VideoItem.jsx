import React from 'react';
import cl from './VideoItem.module.css'
import reactStringReplace from 'react-string-replace'

const VideoItem = ({video, text}) => {
    return (
        <div className={cl.video__container}>
            <div className={cl.video__image}><img src={video.video.thumbnail.thumbnails[2].url} alt="" /></div>
            <div className={cl.video__info}>
                <div className={cl.profile__img}>
                    <img src="" alt="" />
                </div>
                <div className={cl.video__title__block}>
                    <span className={cl.video__title}>{video.video.title}</span>
                    <div className={cl.video__title__block__info}>
                        <span>{video.video.username}</span>
                    </div>
                </div>
            </div>
            <div className={cl.lines__block}>
                <table className={cl.lines__table}>
                {video.transcription.map(line => 
                    <tr>
                        <td className={cl.timecode}>
                            <a target='_blank' href={"https://youtube.com/watch?v=" + video.video.video_id + "&t=" + Math.round(line.startMs / 1000)}>{(new Date(line.startMs).toISOString().substr(14, 5))} </a>
                        </td>
                        <td>
                            <i>
                                {
                                    reactStringReplace(line.text, text, () => (
                                        <span className={cl.highlighted__text}>{text}</span>
                                    ))
                                }</i>
                        </td>
                    </tr>
                )}
                </table>
            </div>
        </div>
    );
}

export default VideoItem;
