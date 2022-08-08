import { Button, Layout } from 'antd'
import Text from 'antd/lib/typography/Text'
import { FC } from 'react'

export interface ISiteFooterProps {}

export const SiteFooter: FC<ISiteFooterProps> = ({}: ISiteFooterProps) => {
  return (
    <Layout.Footer style={{ textAlign: 'center' }}>
      <Button type="link">
        <Text underline>CGU</Text>
      </Button>
      <Button type="link">
        <Text underline>Legal Notice</Text>
      </Button>
      <Button type="link">
        <Text underline>Contact</Text>
      </Button>
    </Layout.Footer>
  )
}

SiteFooter.displayName = 'SiteFooter'

export default SiteFooter
