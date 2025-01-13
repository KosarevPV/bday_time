
    'use strict';

    const Heading = ({ date, changeMonth, resetDate }) => (
        <nav className="calendar--nav">
            <a onClick={() => changeMonth(date.month() - 1)}>&#8249;</a>
            <h1 onClick={() => resetDate()}>{date.format('MMMM')} <small>{date.format('YYYY')}</small></h1>
            <a onClick={() => changeMonth(date.month() + 1)}>&#8250;</a>
        </nav>
    );

    const Day = ({ currentDate, date, startDate, endDate, onClick }) => {
        let className = [];

        const data = window.data
        const isBday = data.some(bdate => {
            return (
                bdate.day === date.date().toString() &&
                bdate.month === (date.month() + 1).toString()
            );
        });
    
        if (isBday && moment().isSame(date, 'day')) {
            className.push('active-bday');
        }
        else if ((moment().isSame(date, 'day'))) {
            console.log(isBday);
            className.push('active');
        }
        else if (!date.isSame(currentDate, 'month') && isBday) {
            className.push('muted-bday');
        }
        else if (isBday) {
            className.push('bday');
        }
        else if (!date.isSame(currentDate, 'month')){
            className.push('muted');
        };

        return (
            <span onClick={() => onClick(date)} className={className.join(' ')}>{date.date()}</span>
        );
    };

    const Days = ({ date, onClick }) => {
        const thisDate = moment(date);
        const daysInMonth = moment(date).daysInMonth();
        const firstDayDate = moment(date).startOf('month');
        const previousMonth = moment(date).subtract(1, 'month');
        const previousMonthDays = previousMonth.daysInMonth();
        const nextsMonth = moment(date).add(1, 'month');
        let days = [];
        let labels = [];

        for (let i = 1; i <= 7; i++) {
            labels.push(<span key={`label-${i}`} className="label">{moment().day(i).format('ddd')}</span>);
        }

        for (let i = firstDayDate.day(); i > 1; i--) {
            previousMonth.date(previousMonthDays - i + 2);

            days.push(
                <Day key={`prev-${moment(previousMonth).format('DD-MM-YYYY')}-${i}`} onClick={(date) => onClick(date)} currentDate={date} date={moment(previousMonth)} />
            );
        }

        for (let i = 1; i <= daysInMonth; i++) {
            thisDate.date(i);

            days.push(
                <Day key={`curr-${moment(thisDate).format('DD-MM-YYYY')}-${i}`} onClick={(date) => onClick(date)} currentDate={date} date={moment(thisDate)} />
            );
        }

        const daysCount = days.length;
        for (let i = 1; i <= (42 - daysCount); i++) {
            nextsMonth.date(i);
            days.push(
                <Day key={`next-${moment(nextsMonth).format('DD-MM-YYYY')}-${i}`} onClick={(date) => onClick(date)} currentDate={date} date={moment(nextsMonth)} />
            );
        }

        return (
            <nav className="calendar--days">
                {labels.concat()}
                {days.concat()}
            </nav>
        );
    };

    class Calendar extends React.Component {
        constructor(props) {
            super(props);
            this.state = {date: moment()};
        }

        resetDate() {
            this.setState({
                date: moment()
            });
        }

        changeMonth(month) {
            const { date } = this.state;

            date.month(month);

            this.setState(date);
        }

        changeDate(date) {
            console.log(date.date());
        }

        render() {
            const { date } = this.state;

            return (
                <div className="calendar">
                    <Heading date={date} changeMonth={(month) => this.changeMonth(month)} resetDate={() => this.resetDate()} />
                    <Days onClick={(date) => this.changeDate(date)} date={date} />
                </div>
            );
        }
    }

    ReactDOM.render(
        <Calendar />,
        document.getElementById('calendar')
    );