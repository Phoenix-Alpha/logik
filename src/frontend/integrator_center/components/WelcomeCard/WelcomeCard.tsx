import { Card, Image } from 'antd'
import { FC } from 'react'

export interface IWelcomeCardProps {}

export const WelcomeCard: FC<IWelcomeCardProps> = ({}: IWelcomeCardProps) => {
  return (
    <Card
      style={{ width: 300 }}
      cover={
        <Image
          width={300}
          alt="welcome-card-alt"
          src="https://gw.alipayobjects.com/zos/rmsportal/JiqGstEfoWAOHiTxclqi.png"
        />
      }
    >
      We supply a series of design principles, practical patterns and high
      quality design resources (Sketch and Axure), to help people create their
      product prototypes beautifully and efficiently.
    </Card>
  )
}


WelcomeCard.displayName = 'WelcomeCard'

export default WelcomeCard
